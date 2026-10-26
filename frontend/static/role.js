function normalizeRole(v){
  const x=(v||"").toLowerCase();
  if(x==="admin") return "admin";
  if(x==="dosen") return "dosen";
  if(x==="mahasiswa") return "mahasiswa";
  return "";
}
function currentRole(){ return normalizeRole(localStorage.getItem("role")); }
function currentName(){ return localStorage.getItem("student_name") || localStorage.getItem("user_name") || "Pengguna"; }

function roleHome(role=currentRole()){
  if(role==="admin") return "/admin-dashboard.html";
  if(role==="dosen") return "/dosen-dashboard.html";
  if(role==="mahasiswa") return "/mahasiswa-dashboard.html";
  return "/login.html";
}
function requireRole(expected){
  const role=currentRole();
  if(!role){ location.href="/login.html"; return false; }
  if(expected && role!==expected){ location.href=roleHome(role); return false; }
  return true;
}
function loginByRole(){
  const role=normalizeRole(document.getElementById("role").value);
  const name=(document.getElementById("login_name")?.value || "").trim() || (role==="admin"?"Administrator":role==="dosen"?"Dosen":"Mahasiswa");
  localStorage.setItem("role",role);
  localStorage.setItem("user_name",name);
  localStorage.setItem("student_name",name);
  location.href=roleHome(role);
}
function logoutRole(){ localStorage.clear(); location.href="/login.html"; }

document.addEventListener("DOMContentLoaded",()=>{
  document.querySelectorAll("[data-user-name]").forEach(e=>e.textContent=currentName());
  document.querySelectorAll("[data-role-name]").forEach(e=>e.textContent=currentRole()||"-");
});
