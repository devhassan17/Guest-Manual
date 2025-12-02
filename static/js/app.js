(function(){
  const params = new URLSearchParams(location.search);
  const t = params.get('theme');
  if(t){ document.documentElement.classList.add('theme-'+t); }
})();
document.addEventListener('DOMContentLoaded', () => {
  const gallery = document.querySelectorAll('#gallery img[data-maybe]');
  gallery.forEach(img => {
    const url = img.getAttribute('data-maybe'); if(!url) return;
    img.src = url; img.onerror = () => { const ph = img.closest('.ph'); if(ph) ph.style.display='none'; };
    img.onclick = () => openLightbox(url);
  });
});
function openLightbox(src){
  let lb = document.getElementById('lightbox');
  if(!lb){
    lb = document.createElement('div');
    lb.id = 'lightbox';
    Object.assign(lb.style, {position:'fixed', inset:'0', background:'rgba(0,0,0,.82)', display:'flex', alignItems:'center', justifyContent:'center', zIndex:'9999'});
    lb.addEventListener('click', ()=> lb.remove());
    const img = document.createElement('img');
    Object.assign(img.style, {maxWidth:'92vw', maxHeight:'92vh', borderRadius:'12px', boxShadow:'0 20px 60px rgba(0,0,0,.5)'});
    lb.appendChild(img);
    document.body.appendChild(lb);
  }
  lb.querySelector('img').src = src;
  lb.style.display = 'flex';
}


// Enhance property navigation: load sections without full page refresh
document.addEventListener('DOMContentLoaded', () => {
  const main = document.querySelector('main.container');
  if (!main) return;

  function attachPropNavHandlers() {
    const nav = main.querySelector('.prop-nav');
    if (!nav) return;
    nav.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', (e) => {
        const href = link.getAttribute('href');
        if (!href) return;
        // Let modified/blank-target clicks behave normally
        if (link.target === '_blank' || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;

        e.preventDefault();
        fetch(href, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
          .then(resp => resp.text())
          .then(html => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const newMain = doc.querySelector('main.container');
            if (!newMain) {
              // Fallback: if something went wrong, just navigate normally
              window.location.href = href;
              return;
            }
            main.innerHTML = newMain.innerHTML;
            history.pushState({ url: href }, '', href);
            attachPropNavHandlers();
            window.scrollTo({ top: 0, behavior: 'smooth' });
          })
          .catch(() => {
            window.location.href = href;
          });
      });
    });
  }

  attachPropNavHandlers();

  window.addEventListener('popstate', (event) => {
    const url = (event.state && event.state.url) || window.location.href;
    fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
      .then(resp => resp.text())
      .then(html => {
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const newMain = doc.querySelector('main.container');
        if (!newMain) return;
        main.innerHTML = newMain.innerHTML;
        attachPropNavHandlers();
      })
      .catch(() => {});
  });
});
