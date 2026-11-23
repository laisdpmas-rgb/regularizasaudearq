// Eventos para o dataLayer. Inerte até existir um GTM/GA4 na página: não instala nenhuma tag.
// Abrir o WhatsApp mede o clique, não um lead recebido.
(function () {
  window.dataLayer = window.dataLayer || [];
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
