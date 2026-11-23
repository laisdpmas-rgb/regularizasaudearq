#!/usr/bin/env python3
"""Confere o que não pode quebrar: número do WhatsApp, JSON-LD, ids repetidos e sitemap. Uso: python3 tools/checar.py"""
import glob, json, os, re, sys
raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(raiz)
erros = []
paginas = ['index.html', 'privacidade.html'] + sorted(glob.glob('*/index.html'))
numero = re.search(r"whatsappNumber:\s*'(\d+)'", open('assets/js/config.js').read()).group(1)
for f in paginas + glob.glob('assets/js/*.js') + ['tools/gerar-paginas.py']:
    for n in re.findall(r'wa\.me/(\d+)', open(f).read()):
        if n != numero: erros.append(f'{f}: número {n} diferente de {numero}')
for f in paginas:
    s = open(f).read()
    for j in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try: json.loads(j)
        except ValueError as e: erros.append(f'{f}: JSON-LD inválido ({e})')
    ids = re.findall(r'\sid="([^"]+)"', s)
    for i in {i for i in ids if ids.count(i) > 1}: erros.append(f'{f}: id repetido "{i}"')
for u in re.findall(r'<loc>https://regularizasaudearq\.com\.br(/[^<]*)</loc>', open('sitemap.xml').read()):
    if not os.path.exists(u.lstrip('/') + ('index.html' if u.endswith('/') else '')): erros.append(f'sitemap: {u} sem arquivo')
print('\n'.join(erros) or 'ok'); sys.exit(1 if erros else 0)
