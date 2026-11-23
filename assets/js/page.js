// Comportamento das páginas internas: menu, links de WhatsApp (número vem de config.js) e botão flutuante.
(function () {
  var cfg = window.RS_CONFIG || {};
  var toggle = document.getElementById('menuToggle'), nav = document.getElementById('navlinks');
  if (toggle && nav) {
    toggle.addEventListener('click', function () { var o = nav.classList.toggle('open'); toggle.setAttribute('aria-expanded', String(o)); toggle.setAttribute('aria-label', o ? 'Fechar menu' : 'Abrir menu'); toggle.textContent = o ? '× Fechar' : '☰ Menu'; });
    nav.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', function () { nav.classList.remove('open'); toggle.setAttribute('aria-expanded', 'false'); toggle.textContent = '☰ Menu'; }); });
  }
  document.querySelectorAll('.whatsapp-link').forEach(function (l) {
    if (!cfg.whatsappNumber) { l.href = '#avaliacao'; return; }
    l.href = 'https://wa.me/' + cfg.whatsappNumber + '?text=' + encodeURIComponent(l.getAttribute('data-message') || '');
    l.target = '_blank'; l.rel = 'noopener noreferrer';
  });
  var y = document.getElementById('year'); if (y) y.textContent = new Date().getFullYear();
  var fc = document.querySelector('.floating-cta');
  if (fc && 'IntersectionObserver' in window) {
    var seen = new Set(), io = new IntersectionObserver(function (es) { es.forEach(function (e) { e.isIntersecting ? seen.add(e.target) : seen.delete(e.target); }); fc.classList.toggle('is-hidden', seen.size > 0); });
    ['.page-hero', '#contato', '.footer'].forEach(function (s) { var el = document.querySelector(s); if (el) io.observe(el); });
  }
})();
