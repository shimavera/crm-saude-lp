#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplica nos 2 posts escritos à mão (sem body em _bodies) o mesmo tratamento
que o _build.py dá aos gerados: autoria Person, caixa de autor, bloco de
fontes, item de TOC e link "Sobre" no rodapé.

Idempotente: roda de novo sem duplicar nada.
"""
import os, re

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "blog")
BASE = "https://saudecrm.com"
DATE_MODIFIED = "2026-08-15"
DATE_MODIFIED_HUMAN = "15 de agosto de 2026"
MARK = "<!-- fontes-externas -->"

AUTHOR_JSON = '''"author": {
      "@type": "Person",
      "@id": "https://saudecrm.com/sobre.html#juan-lourenco",
      "name": "Juan Lourenço",
      "url": "https://saudecrm.com/sobre.html",
      "jobTitle": "Fundador do SaúdeCRM",
      "description": "Acelerador de clínicas odontológicas. Trabalha dentro da operação, em agenda, recepção e funil de leads.",
      "sameAs": ["https://www.instagram.com/juansaraivalourenco/"]
    }'''

AUTHOR_BOX = '''
        <div class="author-box" style="display:flex;gap:18px;align-items:flex-start;background:#fff;border:1px solid #E3E8F2;border-radius:14px;padding:22px 24px;margin:34px 0 8px">
          <img src="/logo.webp" alt="Juan Lourenço" width="56" height="56" style="width:56px;height:56px;border-radius:50%;object-fit:cover;flex:none">
          <div style="font-size:15px;line-height:1.6">
            <div style="font-family:'Plus Jakarta Sans',sans-serif;font-weight:800;font-size:16px;margin-bottom:2px">Juan Lourenço</div>
            <div style="font-size:13px;color:#5A6472;margin-bottom:10px">Fundador do SaúdeCRM · acelerador de clínicas odontológicas</div>
            <p style="margin:0 0 10px;color:#232B39">Trabalha dentro da operação de clínicas: agenda, recepção, funil de leads e fechamento de tratamento. Escreve a partir do que vê se repetir em clínicas diferentes, não de teoria.</p>
            <p style="margin:0;color:#232B39"><a href="/sobre.html" rel="author">Sobre o autor</a> · <a href="https://www.instagram.com/juansaraivalourenco/" rel="me nofollow">@juansaraivalourenco</a></p>
          </div>
        </div>
'''

FONTES = {
    "crm-para-clinica-odontologica": [
        ("https://whatsappbusiness.com/pt-br/policy/", "Política de Mensagens do WhatsApp Business",
         "regras de consentimento (opt-in) e de suspensão de conta"),
        ("https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm", "Lei nº 13.709/2018 (LGPD)",
         "texto integral da lei de proteção de dados"),
        ("https://website.cfo.org.br/codigos/", "Código de Ética Odontológica (CFO)",
         "normas de anúncio, propaganda e publicidade"),
    ],
    "equipe-nao-consegue-acompanhar-leads": [
        ("https://whatsappbusiness.com/pt-br/policy/", "Política de Mensagens do WhatsApp Business",
         "regras de consentimento (opt-in) e de suspensão de conta"),
        ("https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm", "Lei nº 13.709/2018 (LGPD)",
         "texto integral da lei de proteção de dados"),
    ],
}


def bloco_fontes(slug):
    itens = "".join(
        f'            <li><a href="{u}" target="_blank" rel="noopener nofollow">{n}</a> — {d}.</li>\n'
        for u, n, d in FONTES[slug])
    return (f'\n{MARK}\n'
            f'          <h2 id="fontes">Fontes</h2>\n'
            f'          <p>As afirmações sobre regras de plataforma, legislação e normas do conselho neste artigo '
            f'podem ser conferidas nas fontes primárias abaixo.</p>\n'
            f'          <ul>\n{itens}          </ul>\n')


for slug in FONTES:
    path = os.path.join(OUT, f"{slug}.html")
    t = open(path, encoding="utf-8").read()
    orig = t
    mudou = []

    # 1) autoria no schema
    if '"author": {\n      "@type": "Organization",\n      "name": "SaúdeCRM"\n    }' in t:
        t = t.replace('"author": {\n      "@type": "Organization",\n      "name": "SaúdeCRM"\n    }',
                      AUTHOR_JSON, 1)
        mudou.append("schema author")

    # 2) dateModified
    t2 = re.sub(r'"dateModified": "\d{4}-\d{2}-\d{2}"', f'"dateModified": "{DATE_MODIFIED}"', t)
    if t2 != t:
        t = t2
        mudou.append("dateModified")

    # 3) assinatura visível
    if "<span>Por SaúdeCRM</span>" in t:
        t = t.replace(
            "<span>Por SaúdeCRM</span>",
            '<span>Por <a href="/sobre.html" rel="author" style="color:inherit;text-decoration:underline;'
            f'text-underline-offset:2px">Juan Lourenço</a></span>\n            <span class="article-meta-sep">·</span>\n'
            f'            <span>Atualizado em {DATE_MODIFIED_HUMAN}</span>', 1)
        mudou.append("assinatura")

    # 4) fontes + caixa de autor no fim do artigo
    if MARK not in t:
        t = t.replace("        </article>", bloco_fontes(slug) + "        </article>" + AUTHOR_BOX, 1)
        mudou.append("fontes + caixa de autor")

    # 5) item de TOC
    if 'href="#fontes"' not in t:
        m = re.search(r'(<ul class="toc-list">.*?)(\n\s*</ul>)', t, re.S)
        if m:
            t = t[:m.end(1)] + '\n            <li><a href="#fontes">Fontes</a></li>' + t[m.end(1):]
            mudou.append("toc")

    # 6) link Sobre no rodapé
    if '<a href="/sobre.html">Sobre</a>' not in t:
        t = t.replace('<a href="/blog/">Blog</a>', '<a href="/blog/">Blog</a>\n          <a href="/sobre.html">Sobre</a>', 1)
        mudou.append("footer sobre")

    if t != orig:
        open(path, "w", encoding="utf-8").write(t)
        print(f"OK {slug}: {', '.join(mudou)}")
    else:
        print(f"== {slug}: nada a fazer")
