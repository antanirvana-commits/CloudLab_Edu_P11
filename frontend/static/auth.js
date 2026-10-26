const AUTH_KEY="cloudlab_auth";

function authState(){
  try{return JSON.parse(localStorage.getItem(AUTH_KEY)||"null");}catch{return null;}
}
function authToken(){return authState()?.access_token||"";}
function currentUser(){return authState()?.user||null;}
function roleHome(role=currentUser()?.role){
  if(role==="admin") return "/admin/index.html";
  if(role==="dosen") return "/dosen/index.html";
  if(role==="mahasiswa") return "/mahasiswa/index.html";
  return "/public/login.html";
}

async function readResponse(response){
  const text=await response.text();
  if(!text)return {};
  try{return JSON.parse(text);}catch{return {detail:text};}
}

function apiErrorMessage(data,status){
  const detail=data?.detail;
  if(typeof detail==="string" && detail.trim()) return detail;
  if(Array.isArray(detail)){
    const msgs=detail.map(item=>item?.msg||item?.message).filter(Boolean);
    if(msgs.length)return msgs.join("; ");
  }
  if(data?.error && typeof data.error==="string") return data.error.replaceAll("_"," ");
  return `Permintaan gagal (HTTP ${status}).`;
}

async function apiRequest(url,opts={}){
  const headers={...(opts.headers||{})};
  if(opts.body && !headers["Content-Type"]) headers["Content-Type"]="application/json";
  const token=authToken();
  if(token)headers.Authorization=`Bearer ${token}`;

  let response;
  try{
    response=await fetch(url,{...opts,headers,credentials:"same-origin"});
  }catch{
    throw new Error("Tidak dapat terhubung ke server CloudLab Edu.");
  }

  const data=await readResponse(response);
  if(response.status===401){
    localStorage.removeItem(AUTH_KEY);
    const message=apiErrorMessage(data,response.status);
    if(!location.pathname.includes("/public/login")) location.href="/public/login.html?session=expired";
    throw new Error(message);
  }
  if(response.status===403) throw new Error(apiErrorMessage(data,response.status));
  if(!response.ok) throw new Error(apiErrorMessage(data,response.status));
  return data;
}

async function login(){
  const username=document.getElementById("login_username").value.trim();
  const password=document.getElementById("login_password").value;
  const note=document.getElementById("login_note");
  note.className="notice"; note.textContent="";

  if(!username || !password){
    note.className="notice err";
    note.textContent="Username/email dan password wajib diisi.";
    return;
  }

  try{
    const data=await apiRequest("/api/auth/login",{method:"POST",body:JSON.stringify({username,password})});
    localStorage.setItem(AUTH_KEY,JSON.stringify(data));
    location.href=roleHome(data.user.role);
  }catch(e){
    note.className="notice err";
    note.textContent=e?.message||"Login gagal.";
  }
}

async function resumeSession(){
  if(!authToken()) return false;
  try{
    const user=await apiRequest("/api/auth/me");
    const state=authState()||{};
    state.user=user;
    localStorage.setItem(AUTH_KEY,JSON.stringify(state));
    location.href=roleHome(user.role);
    return true;
  }catch{
    localStorage.removeItem(AUTH_KEY);
    return false;
  }
}

async function logout(){
  try{await fetch("/api/auth/logout",{method:"POST",credentials:"same-origin"});}catch{}
  localStorage.removeItem(AUTH_KEY);
  location.href="/public/login.html";
}

function requireRole(expected){
  const user=currentUser();
  if(!user||!authToken()){
    location.href="/public/login.html";
    return false;
  }
  const allowed=Array.isArray(expected)?expected:[expected];
  if(expected&&!allowed.includes(user.role)){
    location.href="/public/403.html";
    return false;
  }
  // Validasi token ke server agar session lama tidak dianggap masih aktif.
  refreshMe().catch(()=>{});
  return true;
}

function openAdminDocs(){
  const u=currentUser();
  if(!u||u.role!=="admin")return;
  window.open("/docs","_blank","noopener");
}

async function refreshMe(){
  const data=await apiRequest("/api/auth/me");
  const state=authState()||{};
  state.user=data;
  localStorage.setItem(AUTH_KEY,JSON.stringify(state));
  return data;
}

async function loadProfile(){
  const form=document.getElementById("profileForm");if(!form)return;
  try{
    const u=await refreshMe();
    profile_username.value=u.username;
    profile_name.value=u.full_name;
    profile_email.value=u.email;
    profile_role.value=u.role;
  }catch(e){showNotice("profile_note",e.message,false)}
}

async function saveProfile(){
  try{
    const u=await apiRequest("/api/auth/me",{method:"PATCH",body:JSON.stringify({full_name:profile_name.value,email:profile_email.value})});
    const state=authState()||{};
    state.user=u;
    localStorage.setItem(AUTH_KEY,JSON.stringify(state));
    hydrateUser();showNotice("profile_note","Profil berhasil diperbarui.",true);
  }catch(e){showNotice("profile_note",e.message,false)}
}

function showNotice(id,msg,ok=true){
  const e=document.getElementById(id);if(!e)return;
  e.textContent=msg;e.className="notice "+(ok?"ok":"err");
}

function hydrateUser(){
  const u=currentUser();if(!u)return;
  document.querySelectorAll("[data-user-name]").forEach(e=>e.textContent=u.full_name);
  document.querySelectorAll("[data-role-name]").forEach(e=>e.textContent=u.role.charAt(0).toUpperCase()+u.role.slice(1));
  document.querySelectorAll("[data-user-email]").forEach(e=>e.textContent=u.email);
  document.querySelectorAll("[data-avatar]").forEach(e=>e.textContent=(u.full_name||"CL").split(/\s+/).slice(0,2).map(x=>x[0]).join("").toUpperCase());
}

document.addEventListener("DOMContentLoaded",()=>{
  hydrateUser();loadProfile();
  const p=document.getElementById("login_password");
  if(p)p.addEventListener("keydown",e=>{if(e.key==="Enter")login();});
});
