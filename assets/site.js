(function(){
 // mobile menu
 var b=document.querySelector('.menu-toggle'),n=document.querySelector('.nav');
 if(b&&n){
  b.addEventListener('click',function(){var o=b.getAttribute('aria-expanded')==='true';b.setAttribute('aria-expanded',String(!o));b.setAttribute('aria-label',o?'Menü öffnen':'Menü schließen');n.classList.toggle('open',!o)});
  n.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){b.setAttribute('aria-expanded','false');n.classList.remove('open')})});
 }
 // reveal on scroll
 var els=document.querySelectorAll('.reveal');
 if('IntersectionObserver' in window){
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});
  els.forEach(function(el){io.observe(el)});
 }else{els.forEach(function(el){el.classList.add('in')})}
 // lightbox
 var d=document.querySelector('.lightbox');
 if(d&&d.showModal){
  var li=d.querySelector('img');
  document.addEventListener('click',function(e){
   var t=e.target.closest('img[data-full]');
   if(t){li.src=t.getAttribute('data-full');li.alt=t.alt;d.showModal();return}
   if(e.target===d||e.target.closest('.lb-close'))d.close();
  });
 }
 // contact form: time stamp for spam protection
 var t=document.getElementById('f-ts');if(t)t.value=Math.floor(Date.now()/1000);
})();
