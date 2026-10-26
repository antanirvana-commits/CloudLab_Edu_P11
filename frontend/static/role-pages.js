async function loadRoleDashboard(){
  if(typeof request!=="function") return;
  try{
    const s=await request("/api/dashboard/summary");
    for(const k in s){
      document.querySelectorAll(`[data-metric="${k}"]`).forEach(e=>e.textContent=s[k]);
    }
    const rp=document.getElementById("recent-practicums");
    if(rp){
      const ps=await request("/api/practicums");
      rp.innerHTML=ps.slice(0,5).map(x=>`<tr><td>${esc(x.title)}</td><td>${fmtDate(x.deadline)}</td><td><span class="badge green">Aktif</span></td><td><a class="btn btn-secondary" href="/practicum-detail.html?id=${x.id}">Detail</a></td></tr>`).join("")||`<tr><td colspan="4" class="empty">Belum ada praktikum.</td></tr>`;
    }
    const sp=document.getElementById("studentProgressMetric");
    if(sp){
      const p=await request("/api/labs/lab-p10/progress");
      sp.textContent=p.progress+"%";
    }
  }catch(e){console.error(e)}
}
async function loadAdminUsers(){
  const tb=document.getElementById("adminStudentRows"); if(!tb||typeof request!=="function")return;
  try{
    const rows=await request("/api/students");
    tb.innerHTML=rows.map(x=>`<tr><td>${x.id}</td><td>${esc(x.nim)}</td><td>${esc(x.name)}</td><td>${esc(x.email)}</td><td><span class="role-chip role-mahasiswa">Mahasiswa</span></td></tr>`).join("")||`<tr><td colspan="5" class="empty">Belum ada mahasiswa.</td></tr>`;
  }catch(e){tb.innerHTML=`<tr><td colspan="5">${esc(e.message)}</td></tr>`}
}
async function loadStudentPracticums(){
  const tb=document.getElementById("studentPracticumRows");if(!tb||typeof request!=="function")return;
  try{
    const rows=await request("/api/practicums");
    tb.innerHTML=rows.map(x=>`<tr><td>${x.id}</td><td>${esc(x.title)}</td><td>${esc(x.description)}</td><td>${fmtDate(x.deadline)}</td><td><span class="badge green">Tersedia</span></td></tr>`).join("")||`<tr><td colspan="5" class="empty">Belum ada praktikum.</td></tr>`;
  }catch(e){console.error(e)}
}
async function loadStudentProgress(){
  if(!document.getElementById("studentProgressBar")||typeof request!=="function")return;
  try{
    const p=await request("/api/labs/lab-p10/progress");
    studentProgressBar.style.width=p.progress+"%";
    studentProgressText.textContent=p.progress+"% ("+p.completed+"/"+p.total+" langkah)";
    studentScore.textContent=p.score+"/"+p.max_score;
  }catch(e){console.error(e)}
}
document.addEventListener("DOMContentLoaded",()=>{
  loadRoleDashboard();
  loadAdminUsers();
  loadStudentPracticums();
  loadStudentProgress();
});
