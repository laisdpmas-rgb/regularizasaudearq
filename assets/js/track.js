// Eventos para o dataLayer. Inerte enquanto gtmId (config.js) estiver vazio: não instala nenhuma tag.
// Abrir o WhatsApp mede o clique, não um lead recebido.
(function () {
  window.dataLayer = window.dataLayer || [];
  // Só carrega o GTM se houver um ID válido em config.js; sem ID, nada é enviado a terceiros.
  var gtm = (window.RS_CONFIG || {}).gtmId;
  if (gtm && /^GTM-[A-Z0-9]+$/.test(gtm)) {
    window.dataLayer.push({ 'gtm.start': Date.now(), event: 'gtm.js' });
    var s = document.createElement('script'); s.async = true;
    s.src = 'https://www.googletagmanager.com/gtm.js?id=' + gtm;
    document.head.appendChild(s);
  }
  var pageId = document.documentElement.getAttribute('data-page') || 'home';
  if (document.documentElement.getAttribute('data-page')) window.dataLayer.push({ event: 'page_view_estrategica', page_id: pageId, page_path: location.pathname });
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a.whatsapp-link');
    if (!a) return;
    var base = { page_id: pageId, cta_location: a.getAttribute('data-cta-location') || '' };
    window.dataLayer.push(Object.assign({ event: 'click_whatsapp' }, base));
    var t = a.getAttribute('data-track');
    if (t) window.dataLayer.push(Object.assign({ event: t }, base));
  });
})();
