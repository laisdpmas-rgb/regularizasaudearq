// Medição: GA4 carregado direto, só depois do aceite de cookies. Sem aceite, nada é enviado ao Google.
// Os eventos também vão para o dataLayer (inerte sem GTM). Abrir o WhatsApp mede o clique, não um lead recebido.
(function () {
  var cfg = window.RS_CONFIG || {}, KEY = 'rs_consent';
  window.dataLayer = window.dataLayer || [];
  var pageId = document.documentElement.getAttribute('data-page') || 'home', ga = false;

  function stored() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function store(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }

  // Origem do anúncio: guarda utm_* e gclid da URL (só nesta sessão) e devolve uma linha para o fim da mensagem do WhatsApp.
  var OK = /^[A-Za-z0-9_.~%+\-]{1,100}$/;
  (function () {
    var q = new URLSearchParams(location.search), o = {};
    ['utm_source', 'utm_medium', 'utm_campaign', 'gclid'].forEach(function (k) { var v = q.get(k); if (v && OK.test(v)) o[k] = v; });
    if (Object.keys(o).length) { try { sessionStorage.setItem('rs_origem', JSON.stringify(o)); } catch (e) {} }
  })();
  window.rsOrigem = function () {
    var o = {}; try { o = JSON.parse(sessionStorage.getItem('rs_origem') || '{}'); } catch (e) {}
    var campanha = [o.utm_source, o.utm_medium, o.utm_campaign].filter(Boolean).join(' / '), it = [];
    if (campanha) it.push(campanha); if (o.gclid) it.push('gclid ' + o.gclid);
    return it.length ? '\n\nOrigem: ' + it.join(' | ') : '';
  };

  function track(name, params) {
    var p = Object.assign({ page_id: pageId }, params || {});
    window.dataLayer.push(Object.assign({ event: name }, p));
    if (ga) window.gtag('event', name, p);
  }

  function loadGA() {
    if (ga || !/^G-[A-Z0-9]+$/.test(cfg.gaId || '')) return;
    ga = true;
    window.gtag = function () { window.dataLayer.push(arguments); };
    var s = document.createElement('script'); s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + cfg.gaId;
    document.head.appendChild(s);
    window.gtag('js', new Date());
    // page_view enviado de forma explícita (não depende do envio automático da configuração).
    window.gtag('config', cfg.gaId, { send_page_view: false });
    window.gtag('event', 'page_view', { page_title: document.title, page_location: location.href, page_path: location.pathname });
    if (document.documentElement.getAttribute('data-page')) track('page_view_estrategica', { page_path: location.pathname });
  }

  function banner() {
    var b = document.createElement('div');
    b.className = 'consent'; b.setAttribute('role', 'region'); b.setAttribute('aria-label', 'Aviso de cookies');
    b.innerHTML = '<p>Usamos o Google Analytics para medir visitas e cliques nos botões de contato. Você aceita? <a href="/privacidade.html">Política de Privacidade</a></p>' +
      '<div class="consent-actions"><button type="button" class="btn btn-accent" data-c="granted">Aceitar</button><button type="button" class="btn btn-outline" data-c="denied">Recusar</button></div>';
    b.addEventListener('click', function (e) {
      var v = e.target.getAttribute && e.target.getAttribute('data-c'); if (!v) return;
      store(v); b.remove(); if (v === 'granted') loadGA();
    });
    document.body.appendChild(b);
  }

  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a.whatsapp-link'); if (!a) return;
    var loc = a.getAttribute('data-cta-location') || '';
    track('click_whatsapp', { cta_location: loc });
    var t = a.getAttribute('data-track'); if (t) track(t, { cta_location: loc });
  });

  var c = stored();
  if (c === 'granted') loadGA(); else if (c !== 'denied' && cfg.gaId) { if (document.body) banner(); else document.addEventListener('DOMContentLoaded', banner); }
})();
