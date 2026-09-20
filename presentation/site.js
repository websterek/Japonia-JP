(() => {
  'use strict';
  document.querySelectorAll('[data-gallery]').forEach((gallery) => {
    const slides=[...gallery.querySelectorAll('.gallery-slide')];
    const thumbs=[...gallery.querySelectorAll('[data-gallery-to]')];
    const counter=gallery.querySelector('[data-gallery-counter]');
    const prev=gallery.querySelector('[data-gallery-prev]');
    const next=gallery.querySelector('[data-gallery-next]');
    if (!slides.length) return;
    let current=0;
    const show=(index) => {
      current=(index+slides.length)%slides.length;
      slides.forEach((slide,i)=>slide.classList.toggle('is-active',i===current));
      thumbs.forEach((thumb,i)=>{
        const active=i===current;
        thumb.classList.toggle('is-active',active);
        thumb.setAttribute('aria-pressed',String(active));
      });
      if(counter) counter.textContent=(current+1)+' / '+slides.length;
    };
    prev?.addEventListener('click',()=>show(current-1));
    next?.addEventListener('click',()=>show(current+1));
    thumbs.forEach((thumb,i)=>thumb.addEventListener('click',()=>show(i)));
    gallery.addEventListener('keydown',(event)=>{
      if(event.target.matches('button,a,input,textarea,select')) return;
      if(event.key==='ArrowLeft'){event.preventDefault();show(current-1);}
      if(event.key==='ArrowRight'){event.preventDefault();show(current+1);}
      if(event.key==='Home'){event.preventDefault();show(0);}
      if(event.key==='End'){event.preventDefault();show(slides.length-1);}
    });
  });
})();