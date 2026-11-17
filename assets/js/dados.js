// TODO-FINAL: preencher antes de publicar. Campo vazio não aparece na página.
// Cada elemento com data-dado="cau" ou data-dado="cnpj" recebe o valor abaixo.
window.DADOS_PROFISSIONAIS = { cau: '', cnpj: '' };
document.querySelectorAll('[data-dado]').forEach(function (el) {
  var v = window.DADOS_PROFISSIONAIS[el.dataset.dado];
  if (v) { el.textContent = (el.dataset.prefixo || '') + v; el.hidden = false; }
});
