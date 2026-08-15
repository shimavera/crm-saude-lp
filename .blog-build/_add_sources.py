#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Insere fontes externas verificadas nos corpos dos artigos.

Duas coisas por artigo:
  1) links inline nas âncoras onde o texto já faz afirmação normativa;
  2) um bloco "Fontes" no fim do corpo.

Idempotente: se o bloco de fontes já existe, o artigo é pulado.
Todas as URLs foram verificadas (HTTP 200) em 15/08/2026.
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
BODIES = os.path.join(HERE, "_bodies")

MARK = '<!-- fontes-externas -->'

S = {
    "wa_policy": ("https://whatsappbusiness.com/pt-br/policy/",
                  "Política de Mensagens do WhatsApp Business",
                  "regras de consentimento (opt-in) e de suspensão de conta"),
    "wa_pricing": ("https://developers.facebook.com/docs/whatsapp/pricing",
                   "Preços da API do WhatsApp Business (Meta for Developers)",
                   "como a Meta cobra pelas conversas na API oficial"),
    "lgpd": ("https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm",
             "Lei nº 13.709/2018 (LGPD)",
             "texto integral da lei de proteção de dados"),
    "cdc": ("https://www.planalto.gov.br/ccivil_03/leis/l8078compilado.htm",
            "Código de Defesa do Consumidor (Lei nº 8.078/1990)",
            "art. 37 trata de publicidade enganosa"),
    "cfo_codigos": ("https://website.cfo.org.br/codigos/",
                    "Código de Ética Odontológica (CFO)",
                    "normas de anúncio, propaganda e publicidade"),
    "cfo_196": ("https://website.cfo.org.br/resolucao-cfo-196-2019/",
                "Resolução CFO-196/2019",
                "regras para divulgação de imagens de tratamentos"),
    "cfo_estat": ("https://website.cfo.org.br/estatisticas/",
                  "Estatísticas do CFO",
                  "profissionais e entidades ativas no Brasil"),
}

# fontes do bloco final, por slug
SOURCES = {
    "automacao-de-whatsapp-para-clinicas": ["wa_policy", "wa_pricing", "lgpd"],
    "como-nao-perder-leads-no-whatsapp": ["wa_policy", "lgpd"],
    "trafego-pago-para-dentistas": ["cfo_codigos", "cfo_196", "cdc"],
    "como-atrair-pacientes-clinica-odontologica": ["cfo_codigos", "cfo_196", "cfo_estat"],
    "follow-up-de-pacientes": ["wa_policy", "lgpd"],
    "crm-para-clinica-de-estetica": ["wa_policy", "lgpd", "cdc"],
    "como-reduzir-faltas-no-show-consultas": ["wa_policy", "lgpd"],
    "funil-de-vendas-para-clinicas": ["wa_policy", "lgpd"],
    "indicadores-clinica-odontologica": ["cfo_estat", "lgpd"],
    "secretaria-ou-crm-atendimento-clinica": ["wa_policy", "lgpd"],
    "crm-para-dentistas": ["wa_policy", "cfo_codigos", "lgpd"],
    "precificacao-consulta-clinica-medica": ["cdc", "lgpd"],
    "precificacao-procedimentos-esteticos": ["cdc", "cfo_196"],
    "gestao-de-clinicas-guia": ["lgpd", "wa_policy"],
    "equipe-minima-para-clinica": ["lgpd", "wa_policy"],
}

# links inline: (slug, trecho exato a substituir, trecho novo)
INLINE = [
    ("automacao-de-whatsapp-para-clinicas",
     "listas compradas e envios em massa sem consentimento podem fazer o WhatsApp suspender o número da clínica",
     'listas compradas e envios em massa sem consentimento podem fazer o WhatsApp suspender o número da clínica '
     '(a <a href="https://whatsappbusiness.com/pt-br/policy/" target="_blank" rel="noopener nofollow">Política de Mensagens do WhatsApp Business</a> '
     'exige opt-in do destinatário e prevê o encerramento da conta em caso de violação)'),
    ("automacao-de-whatsapp-para-clinicas",
     "é a solução homologada pela própria plataforma, voltada para empresas, com regras claras de uso e maior estabilidade",
     'é a solução homologada pela própria plataforma, voltada para empresas, com regras claras de uso e maior estabilidade '
     '(a Meta <a href="https://developers.facebook.com/docs/whatsapp/pricing" target="_blank" rel="noopener nofollow">cobra por conversa</a>, '
     'segundo a tabela oficial)'),
    ("trafego-pago-para-dentistas",
     "precisa respeitar o que estabelecem o Conselho Federal de Odontologia (CFO) e os conselhos regionais",
     'precisa respeitar o que estabelecem o '
     '<a href="https://website.cfo.org.br/codigos/" target="_blank" rel="noopener nofollow">Código de Ética Odontológica</a> '
     'do Conselho Federal de Odontologia (CFO) e os conselhos regionais'),
    ("trafego-pago-para-dentistas",
     "O recomendável é consultar as normas vigentes do CFO",
     'O recomendável é consultar as normas vigentes do CFO, como a '
     '<a href="https://website.cfo.org.br/resolucao-cfo-196-2019/" target="_blank" rel="noopener nofollow">Resolução CFO-196/2019</a>, '
     'que trata da divulgação de imagens de tratamento'),
]


def bloco(slug):
    itens = ""
    for k in SOURCES[slug]:
        url, nome, desc = S[k]
        itens += (f'            <li><a href="{url}" target="_blank" rel="noopener nofollow">{nome}</a> — {desc}.</li>\n')
    return (f'\n{MARK}\n'
            f'        <h2 id="fontes">Fontes</h2>\n'
            f'        <p>As afirmações sobre regras de plataforma, legislação e normas do conselho neste artigo '
            f'podem ser conferidas nas fontes primárias abaixo.</p>\n'
            f'        <ul>\n{itens}        </ul>\n')


def main():
    inline_por_slug = {}
    for slug, old, new in INLINE:
        inline_por_slug.setdefault(slug, []).append((old, new))

    for slug in sorted(SOURCES):
        path = os.path.join(BODIES, f"{slug}.body.html")
        if not os.path.exists(path):
            print(f"-- {slug}: sem body, pulado")
            continue
        txt = open(path, encoding="utf-8").read()
        if MARK in txt:
            print(f"== {slug}: já tem fontes, pulado")
            continue

        n_inline = 0
        for old, new in inline_por_slug.get(slug, []):
            if old not in txt:
                raise SystemExit(f"ERRO: âncora não encontrada em {slug}:\n  {old[:80]}")
            txt = txt.replace(old, new, 1)
            n_inline += 1

        txt = txt.rstrip() + "\n" + bloco(slug)
        open(path, "w", encoding="utf-8").write(txt)
        print(f"OK {slug}: {n_inline} link(s) inline + {len(SOURCES[slug])} fontes")


if __name__ == "__main__":
    main()
