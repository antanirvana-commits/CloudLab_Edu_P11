(function(){
  function normalize(p){ return (p||"").replace(/\/$/,"") || "/"; }

  function ensureAdminDeveloperLab(){
    if(!location.pathname.startsWith("/admin/")) return;
    const groups=[...document.querySelectorAll(".nav-group")];
    const devGroup=groups.find(g=>{
      const label=g.querySelector(".nav-label")?.textContent?.trim().toLowerCase();
      return label==="developer";
    });
    if(!devGroup) return;
    const flyout=devGroup.querySelector(".nav-flyout");
    if(!flyout) return;
    if(flyout.querySelector('a[href="/admin/api-lab.html"]')) return;

    const link=document.createElement("a");
    link.href="/admin/api-lab.html";
    link.setAttribute("data-nav","/admin/api-lab.html");
    link.innerHTML='<span>🧪</span><span><b>API &amp; Validation Lab</b><small>Demo request, validation, error</small></span>';

    const swagger=[...flyout.querySelectorAll("a")].find(a=>a.textContent.includes("API / Swagger"));
    if(swagger) flyout.insertBefore(link, swagger); else flyout.appendChild(link);
  }

  document.addEventListener("DOMContentLoaded",()=>{
    ensureAdminDeveloperLab();

    const current=normalize(location.pathname);
    document.querySelectorAll("[data-nav]").forEach(link=>{
      const target=normalize(link.getAttribute("data-nav"));
      if(target&&current===target){
        link.classList.add("active");
        const group=link.closest(".nav-group");
        if(group)group.querySelector(".nav-toggle")?.classList.add("active-parent");
      }
    });

    document.querySelectorAll(".nav-toggle").forEach(btn=>{
      btn.addEventListener("click",e=>{
        e.preventDefault();e.stopPropagation();
        const group=btn.closest(".nav-group");
        document.querySelectorAll(".nav-group.open").forEach(g=>{if(g!==group)g.classList.remove("open")});
        group?.classList.toggle("open");
      });
    });

    document.addEventListener("click",()=>document.querySelectorAll(".nav-group.open").forEach(g=>g.classList.remove("open")));
    document.addEventListener("keydown",e=>{if(e.key==="Escape")document.querySelectorAll(".nav-group.open").forEach(g=>g.classList.remove("open"))});
  });
})();
