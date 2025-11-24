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
