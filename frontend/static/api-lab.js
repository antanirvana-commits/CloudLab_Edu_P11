let demoStudentId=null;
function pretty(v){return JSON.stringify(v,null,2)}
async function labFetch(url,opts={}){
  const headers={"Content-Type":"application/json",...(opts.headers||{})};
  const token=authToken();if(token)headers.Authorization=`Bearer ${token}`;
  const r=await fetch(url,{...opts,headers,credentials:"same-origin"});
  const data=await r.json().catch(()=>({}));
  return {status:r.status,statusText:r.statusText,data};
}
function showLab(title,result){
  document.getElementById("labTitle").textContent=title;
  document.getElementById("labOutput").textContent=`HTTP ${result.status} ${result.statusText}\n\n${pretty(result.data)}`;
}
function configItem(label,value){return `<div class="config-item"><small>${esc(label)}</small><strong>${esc(value)}</strong></div>`}
async function loadP10Overview(){
  try{
    const [cfg,arch]=await Promise.all([apiRequest("/api/system/config"),apiRequest("/api/system/architecture")]);
    const c=document.getElementById("p10Config");
    c.innerHTML=[
      configItem("Environment",cfg.application.environment),configItem("Version",cfg.application.version),
      configItem("Database driver",cfg.database.driver),configItem("Database",cfg.database.database),
      configItem("APP_SECRET",cfg.secrets.app_secret),configItem("DB password",cfg.secrets.database_password)
    ].join("");
    const a=document.getElementById("p10Architecture");
    a.innerHTML=`<div class="arch-row"><span>Request flow</span><b>${arch.request_flow.join(" → ")}</b></div><div class="arch-row"><span>Frontend roles</span><b>${arch.frontend_roles.join(" • ")}</b></div><div class="arch-row"><span>Controls</span><b>${arch.controls.join(" • ")}</b></div>`;
  }catch(e){showNotice("page_note",e.message,false)}
}
async function demo201(){
  const t=Date.now().toString().slice(-8);const payload={nim:`P10${t}`,name:"Demo Pertemuan 10",email:`p10.${t}@cloudlab.demo`};
  const r=await labFetch("/api/students",{method:"POST",body:JSON.stringify(payload)});if(r.status===201){demoStudentId=r.data.id;document.getElementById("cleanupBtn").style.display="inline-flex"}showLab("201 • Valid input → resource created",r);
}
async function demo422(){
  const payload={nim:"12",name:"A",email:"bukan-email"};const r=await labFetch("/api/students",{method:"POST",body:JSON.stringify(payload)});showLab("422 • Pydantic menolak input invalid",r);
}
async function demo404(){const r=await labFetch("/api/practicums/999999");showLab("404 • Resource tidak ditemukan",r)}
async function demo409(){
  const u=currentUser();const payload={full_name:u?.full_name||"Administrator CloudLab",email:"dosen@cloudlab.example.com"};const r=await labFetch("/api/auth/me",{method:"PATCH",body:JSON.stringify(payload)});showLab("409 • Email sudah digunakan akun lain",r);
}
async function demo500(){const r=await labFetch("/api/system/demo/failure");showLab(r.status===500?"500 • Simulated staging failure":"Failure demo belum aktif di development",r)}
async function cleanupDemoStudent(){if(!demoStudentId)return;const r=await labFetch(`/api/students/${demoStudentId}`,{method:"DELETE"});showLab("Cleanup • Data demo dihapus",r);demoStudentId=null;document.getElementById("cleanupBtn").style.display="none"}
document.addEventListener("DOMContentLoaded",loadP10Overview);
