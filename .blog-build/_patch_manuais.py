#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplica nos posts escritos à mão (os que NÃO têm body em _bodies e por isso não
passam pelo _build.py) o mesmo tratamento dos gerados: autoria Person, caixa de
autor, assinatura com data, bloco de fontes, item de TOC e link "Sobre" no rodapé.

Sem isso o blog fica com metade dos artigos assinados por pessoa e metade pela
organização, o que enfraquece E-E-A-T justamente onde ele mais conta.

Idempotente: roda de novo sem duplicar nada.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "blog")
BODIES = os.path.join(HERE, "_bodies")
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

S = {
    "wa_policy": ("https://whatsappbusiness.com/pt-br/policy/", "Política de Mensagens do WhatsApp Business",
                  "regras de consentimento (opt-in) e de suspensão de conta"),
    "wa_pricing": ("https://developers.facebook.com/docs/whatsapp/pricing", "Preços da API do WhatsApp Business (Meta for Developers)",
                   "como a Meta cobra pelas conversas na API oficial"),
    "lgpd": ("https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm", "Lei nº 13.709/2018 (LGPD)",
             "texto integral da lei de proteção de dados"),
    "cdc": ("https://www.planalto.gov.br/ccivil_03/leis/l8078compilado.htm", "Código de Defesa do Consumidor (Lei nº 8.078/1990)",
            "art. 37 trata de publicidade enganosa"),
    "cfo_codigos": ("https://website.cfo.org.br/codigos/", "Código de Ética Odontológica (CFO)",
                    "normas de anúncio, propaganda e publicidade"),
    "cfo_196": ("https://website.cfo.org.br/resolucao-cfo-196-2019/", "Resolução CFO-196/2019",
                "regras para divulgação de imagens de tratamentos"),
    "cfo_estat": ("https://website.cfo.org.br/estatisticas/", "Estatísticas do CFO",
                  "profissionais e entidades ativas no Brasil"),
}

# Só entram fontes onde o texto realmente faz afirmação normativa. Link forçado
# em artigo sem base legal não ajuda ninguém e ainda polui o artigo.
FONTES = {
    "crm-para-clinica-odontologica": ["wa_policy", "lgpd", "cfo_codigos"],
    "equipe-nao-consegue-acompanhar-leads": ["wa_policy", "lgpd"],
    "lgpd-para-clinicas": ["lgpd", "cdc"],
    "publicidade-odontologica-o-que-pode": ["cfo_codigos", "cfo_196", "cdc"],
    "captacao-pacientes-harmonizacao-facial": ["cfo_196", "cdc"],
    "melhores-sistemas-para-clinicas": ["wa_policy", "lgpd"],
    "quanto-custa-crm-para-clinica": ["wa_pricing", "wa_policy"],
    "software-de-gestao-ou-crm-para-clinica": ["lgpd", "wa_policy"],
    "secretaria-virtual-com-ia-para-clinicas": ["wa_policy", "lgpd"],
    "recorrencia-em-clinica-de-estetica": ["wa_policy", "lgpd"],
    # sem base normativa: comissao-de-dentistas-como-calcular, precificacao-odontologica-hora-clinica
}


def bloco_fontes(slug, indent="          "):
    itens = "".join(
        f'{indent}  <li><a href="{u}" target="_blank" rel="noopener nofollow">{n}</a> — {d}.</li>\n'
        for u, n, d in (S[k] for k in FONTES[slug]))
    return (f'\n{MARK}\n'
            f'{indent}<h2 id="fontes">Fontes</h2>\n'
            f'{indent}<p>As afirmações sobre regras de plataforma, legislação e normas do conselho neste artigo '
            f'podem ser conferidas nas fontes primárias abaixo.</p>\n'
            f'{indent}<ul>\n{itens}{indent}</ul>\n')


def manuais():
    """Todo post do blog que não é gerado a partir de _bodies."""
    gerados = {f[:-len(".body.html")] for f in os.listdir(BODIES) if f.endswith(".body.html")}
    for f in sorted(os.listdir(OUT)):
        if not f.endswith(".html") or f == "index.html":
            continue
        slug = f[:-len(".html")]
        if slug not in gerados:
            yield slug


def patch(slug):
    path = os.path.join(OUT, f"{slug}.html")
    t = open(path, encoding="utf-8").read()
    orig = t
    feito = []

    # 1) autoria no schema (aceita o formato de uma linha e o multilinha)
    novo, n = re.subn(r'"author":\s*\{\s*"@type":\s*"Organization",\s*"name":\s*"Sa[úu]deCRM"(?:,\s*"url":\s*"[^"]*")?\s*\}',
                      lambda _: AUTHOR_JSON, t, count=1)
    if n:
        t = novo; feito.append("schema author")

    # 2) dateModified
    novo, n = re.subn(r'"dateModified":\s*"\d{4}-\d{2}-\d{2}"', f'"dateModified": "{DATE_MODIFIED}"', t)
    if n:
        t = novo; feito.append("dateModified")

    # 3) assinatura visível
    if "<span>Por SaúdeCRM</span>" in t:
        t = t.replace("<span>Por SaúdeCRM</span>",
                      '<span>Por <a href="/sobre.html" rel="author" style="color:inherit;text-decoration:underline;'
                      'text-underline-offset:2px">Juan Lourenço</a></span>\n            <span class="article-meta-sep">·</span>\n'
                      f'            <span>Atualizado em {DATE_MODIFIED_HUMAN}</span>', 1)
        feito.append("assinatura")

    # 4) fontes + caixa de autor no fim do artigo
    if "</article>" in t:
        add = ""
        if MARK not in t and slug in FONTES:
            add += bloco_fontes(slug)
            feito.append("fontes")
        fecha = "        </article>" if "        </article>" in t else "</article>"
        if "author-box" not in t:
            t = t.replace(fecha, add + fecha + AUTHOR_BOX, 1)
            feito.append("caixa de autor")
        elif add:
            t = t.replace(fecha, add + fecha, 1)

    # 5) item de TOC para as fontes
    if 'href="#fontes"' not in t and 'id="fontes"' in t:
        m = re.search(r'(<ul class="toc-list">.*?)(\n\s*</ul>)', t, re.S)
        if m:
            t = t[:m.end(1)] + '\n            <li><a href="#fontes">Fontes</a></li>' + t[m.end(1):]
            feito.append("toc")

    # 6) link Sobre no rodapé
    if '<a href="/sobre.html">Sobre</a>' not in t and '<a href="/blog/">Blog</a>' in t:
        t = t.replace('<a href="/blog/">Blog</a>', '<a href="/blog/">Blog</a>\n          <a href="/sobre.html">Sobre</a>', 1)
        feito.append("footer sobre")

    if t != orig:
        open(path, "w", encoding="utf-8").write(t)
        print(f"OK {slug}: {', '.join(feito)}")
    else:
        print(f"== {slug}: nada a fazer")


if __name__ == "__main__":
    for slug in manuais():
        patch(slug)
