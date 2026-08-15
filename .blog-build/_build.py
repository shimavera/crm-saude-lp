#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re, os, html, json
from _faq_main import FAQ as FAQ_PUBLICADO

# HERE = onde vivem os fontes do build (_bodies). OUT = onde os .html publicados ficam.
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "blog")
BASE = "https://saudecrm.com"
DATE_ISO = "2026-06-14"
DATE_HUMAN = "14 de junho de 2026"
# Atualizar quando o conteúdo dos posts for revisado de verdade (não a cada build de template)
DATE_MODIFIED = "2026-08-15"
DATE_MODIFIED_HUMAN = "15 de agosto de 2026"

# Extrai o CSS do artigo de referência
ref = open(os.path.join(OUT, "crm-para-clinica-odontologica.html"), encoding="utf-8").read()
css = re.search(r"<style>(.*?)</style>", ref, re.S).group(1)

ARTICLES = [
    {
        "slug": "como-atrair-pacientes-clinica-odontologica",
        "title": "Como Atrair Pacientes para Clínica Odontológica: 12 Estratégias para 2026",
        "seoTitle": "Como Atrair Pacientes para Clínica Odontológica",
        "desc": "Descubra como atrair pacientes para clínica odontológica com 12 estratégias práticas de captação: presença digital, conteúdo, tráfego pago e conversão de leads.",
        "category": "Captação de Pacientes",
        "readTime": 6,
        "heroPills": ["Captação de pacientes", "Marketing odontológico", "Agenda cheia"],
        "toc": [{"id":"presenca-digital","label":"Presença digital"},{"id":"conteudo-redes","label":"Conteúdo e redes sociais"},{"id":"trafego-pago","label":"Tráfego pago"},{"id":"atendimento-conversao","label":"Atendimento e conversão"},{"id":"retencao-indicacao","label":"Retenção e indicação"},{"id":"processos-tecnologia","label":"Processo e tecnologia"},{"id":"conclusao","label":"Conclusão"}],
    },
    {
        "slug": "como-nao-perder-leads-no-whatsapp",
        "title": "Como Não Perder Leads no WhatsApp: O Guia para Clínicas",
        "seoTitle": "Como Não Perder Leads no WhatsApp",
        "desc": "Sua clínica perde leads no WhatsApp? Veja como organizar o atendimento, responder rápido e fazer follow-up para transformar contatos em pacientes agendados.",
        "category": "WhatsApp & Atendimento",
        "readTime": 7,
        "heroPills": ["Atendimento WhatsApp", "Gestão de leads", "Funil de clínica"],
        "toc": [{"id":"por-que-clinicas-perdem-leads","label":"Por que clínicas perdem leads"},{"id":"sinais-do-problema","label":"Sinais do problema"},{"id":"tempo-de-resposta","label":"Tempo de resposta"},{"id":"organizar-por-etapas","label":"Organizar por etapas"},{"id":"follow-up","label":"Follow-up"},{"id":"whatsapp-pessoal-vs-crm","label":"WhatsApp pessoal vs CRM"},{"id":"automacao","label":"Automação inteligente"},{"id":"como-medir","label":"Como medir"},{"id":"conclusao","label":"Conclusão"}],
    },
    {
        "slug": "funil-de-vendas-para-clinicas",
        "title": "Funil de Vendas para Clínicas: Como Transformar Leads em Pacientes",
        "seoTitle": "Funil de Vendas para Clínicas: Guia Completo",
        "desc": "Entenda o que é um funil de vendas para clínicas e como mapear cada etapa — do lead ao paciente fiel — para parar de perder oportunidades e vender mais.",
        "category": "Vendas & Conversão",
        "readTime": 7,
        "heroPills": ["Funil de vendas", "Kanban no CRM", "Mais pacientes"],
        "toc": [{"id":"o-que-e-funil-de-vendas-numa-clinica","label":"O que é um funil de vendas"},{"id":"as-etapas-do-funil","label":"As etapas do funil"},{"id":"como-mapear-seu-funil","label":"Como mapear o funil"},{"id":"gargalos-comuns-no-funil","label":"Gargalos comuns"},{"id":"taxa-de-conversao-por-etapa","label":"Taxa de conversão por etapa"},{"id":"como-usar-kanban-e-crm","label":"Kanban e CRM"},{"id":"erros-comuns-ao-montar-o-funil","label":"Erros comuns"},{"id":"conclusao","label":"Conclusão"}],
    },
    {
        "slug": "automacao-de-whatsapp-para-clinicas",
        "title": "Automação de WhatsApp para Clínicas: O Que É e Como Implementar",
        "seoTitle": "Automação de WhatsApp para Clínicas",
        "desc": "O que é automação de WhatsApp para clínicas, o que dá para automatizar (confirmação, lembrete, follow-up) e como implementar sem parecer robô nem tomar ban.",
        "category": "Automação",
        "readTime": 7,
        "heroPills": ["Automação de WhatsApp", "Atendimento com IA", "Menos faltas"],
        "toc": [{"id":"o-que-e-automacao-de-whatsapp","label":"O que é automação de WhatsApp"},{"id":"o-que-da-pra-automatizar-na-clinica","label":"O que dá pra automatizar"},{"id":"automacao-x-ia-de-atendimento","label":"Automação x IA"},{"id":"riscos-de-fazer-errado","label":"Riscos de fazer errado"},{"id":"api-oficial-vs-nao-oficial","label":"API oficial vs não-oficial"},{"id":"passo-a-passo-de-implementacao","label":"Passo a passo"},{"id":"como-o-saudecrm-faz","label":"Como o SaúdeCRM faz"},{"id":"conclusao","label":"Conclusão"}],
    },
    {
        "slug": "follow-up-de-pacientes",
        "title": "Follow-up de Pacientes: Como Recuperar Leads que Sumiram",
        "seoTitle": "Follow-up de Pacientes: Recupere Leads Sumidos",
        "desc": "Aprenda a fazer follow-up de pacientes e recuperar leads que sumiram: cadência ideal, modelos de mensagem prontos e como automatizar sem perder o tom humano.",
        "category": "Relacionamento",
        "readTime": 7,
        "heroPills": ["Recuperação de leads", "Cadência de WhatsApp", "Modelos prontos"],
        "toc": [{"id":"o-que-e-follow-up","label":"O que é follow-up"},{"id":"por-que-leads-somem","label":"Por que os leads somem"},{"id":"quando-e-quantas-vezes","label":"Quando e quantas vezes"},{"id":"o-que-escrever","label":"O que escrever (modelos)"},{"id":"manual-x-automatico","label":"Manual x automático"},{"id":"reativacao-de-pacientes","label":"Reativação de pacientes"},{"id":"erros-que-afastam","label":"Erros que afastam"},{"id":"como-medir","label":"Como medir"},{"id":"conclusao","label":"Conclusão"}],
    },
    {
        "slug": "como-reduzir-faltas-no-show-consultas",
        "title": "Como Reduzir Faltas (No-Show) em Consultas: 9 Estratégias Práticas",
        "seoTitle": "Como Reduzir Faltas (No-Show) em Consultas",
        "desc": "Como reduzir faltas (no-show) em consultas: 9 estratégias práticas de confirmação, lembrete e relacionamento para manter a agenda da sua clínica cheia.",
        "category": "Gestão de Clínica",
        "readTime": 7,
        "heroPills": ["Reduzir no-show", "Confirmação automática", "Lembretes por WhatsApp"],
        "toc": [{"id":"o-que-e-no-show","label":"O que é no-show"},{"id":"por-que-pacientes-faltam","label":"Por que pacientes faltam"},{"id":"as-9-estrategias","label":"As 9 estratégias"},{"id":"como-juntar-tudo","label":"Como juntar tudo"},{"id":"conclusao","label":"Conclusão"}],
    },
    {
        "slug": "indicadores-clinica-odontologica",
        "title": "Indicadores de uma Clínica Odontológica: O Que Medir para Crescer",
        "seoTitle": "Indicadores de Clínica Odontológica: O Que Medir",
        "desc": "Conheça os indicadores que toda clínica odontológica deveria acompanhar — captação, conversão, no-show, ticket médio e retenção — e como medir cada um.",
        "category": "Gestão de Clínica",
        "readTime": 7,
        "heroPills": ["Gestão de clínica", "KPIs odontológicos", "Crescimento previsível"],
        "toc": [{"id":"por-que-medir-indicadores","label":"Por que medir"},{"id":"indicadores-de-captacao","label":"Captação"},{"id":"indicadores-de-conversao","label":"Conversão"},{"id":"indicadores-de-atendimento","label":"Atendimento"},{"id":"indicadores-operacionais","label":"Operacionais"},{"id":"indicadores-financeiros","label":"Financeiros"},{"id":"indicadores-de-retencao","label":"Retenção"},{"id":"como-acompanhar","label":"Como acompanhar"},{"id":"conclusao","label":"Conclusão"}],
    },
    {
        "slug": "trafego-pago-para-dentistas",
        "title": "Tráfego Pago para Dentistas: Como Transformar Cliques em Pacientes",
        "seoTitle": "Tráfego Pago para Dentistas: Guia Prático",
        "desc": "Tráfego pago para dentistas: por que gerar leads não basta e como transformar cliques do Meta e Google Ads em pacientes que realmente fecham tratamento.",
        "category": "Marketing Digital",
        "readTime": 7,
        "heroPills": ["Tráfego pago", "Meta e Google Ads", "Clique vira paciente"],
        "toc": [{"id":"o-que-e-trafego-pago","label":"O que é tráfego pago"},{"id":"meta-ads-x-google-ads","label":"Meta x Google Ads"},{"id":"o-erro-de-focar-so-em-leads","label":"O erro de focar só em leads"},{"id":"o-que-acontece-depois-do-clique","label":"Depois do clique"},{"id":"trafego-sem-crm","label":"Tráfego sem CRM"},{"id":"como-estruturar-a-captacao","label":"Estruturar a captação"},{"id":"como-medir-o-retorno","label":"Medir o retorno"},{"id":"regras-de-publicidade","label":"Regras de publicidade"},{"id":"conclusao","label":"Conclusão"}],
    },
    {
        "slug": "crm-para-clinica-de-estetica",
        "title": "CRM para Clínica de Estética: Como Organizar Leads e Vender Mais",
        "seoTitle": "CRM para Clínica de Estética: Guia Completo",
        "desc": "CRM para clínica de estética: como organizar os leads do Instagram e WhatsApp, estruturar o funil de vendas e aumentar a recompra e a fidelização.",
        "category": "Guia Completo",
        "readTime": 7,
        "heroPills": ["Instagram e WhatsApp", "Funil da estética", "Recompra previsível"],
        "toc": [{"id":"o-que-e-um-crm-para-clinica-de-estetica","label":"O que é um CRM para estética"},{"id":"particularidades-da-clinica-de-estetica","label":"Particularidades do setor"},{"id":"o-que-um-crm-resolve","label":"O que um CRM resolve"},{"id":"funil-de-vendas-da-estetica","label":"O funil da estética"},{"id":"recompra-e-fidelizacao","label":"Recompra e fidelização"},{"id":"o-que-observar-ao-escolher","label":"O que observar ao escolher"},{"id":"como-implementar","label":"Como implementar"},{"id":"conclusao","label":"Conclusão"}],
    },
    {
        "slug": "secretaria-ou-crm-atendimento-clinica",
        "title": "Secretária ou CRM? Como Organizar o Atendimento da Sua Clínica",
        "seoTitle": "Secretária ou CRM? Como Organizar o Atendimento",
        "desc": "Secretária ou CRM? Entenda como organizar o atendimento da sua clínica unindo a recepção a um CRM para responder rápido, fazer follow-up e não perder pacientes.",
        "category": "Gestão de Clínica",
        "readTime": 7,
        "heroPills": ["Atendimento", "Gestão de clínica", "CRM com WhatsApp"],
        "toc": [{"id":"o-dilema-contratar-ou-investir-em-sistema","label":"O dilema"},{"id":"o-que-sobrecarrega-a-recepcao-hoje","label":"O que sobrecarrega a recepção"},{"id":"o-que-so-o-humano-faz","label":"O que só o humano faz"},{"id":"o-que-o-sistema-faz-melhor-que-humano","label":"O que o sistema faz melhor"},{"id":"como-o-crm-libera-a-secretaria","label":"Como o CRM libera a secretária"},{"id":"sinais-de-que-sua-recepcao-precisa-de-um-crm","label":"Sinais de alerta"},{"id":"como-implementar-sem-assustar-a-equipe","label":"Como implementar"},{"id":"custo-de-uma-contratacao-x-custo-de-um-crm","label":"Custo: contratação x CRM"},{"id":"conclusao","label":"Conclusão"}],
    },
]

by_slug = {a["slug"]: a for a in ARTICLES}
EXISTING = {
    "crm-para-clinica-odontologica": "CRM para Clínica Odontológica: o guia completo",
    "equipe-nao-consegue-acompanhar-leads": "Conflito Marketing vs. Recepção: como resolver",
}

CLARITY = '''  <!-- Microsoft Clarity -->
  <script type="text/javascript">
    (function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);})(window,document,"clarity","script","x70tisywby");
  </script>
  <!-- End Microsoft Clarity -->'''

# Mesmo container da home. Sem isto o blog inteiro fica fora do GA4.
GTM = '''  <!-- Google Tag Manager -->
  <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
  new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
  })(window,document,'script','dataLayer','GTM-5FR2KHPK');</script>
  <!-- End Google Tag Manager -->'''

def esc(s): return html.escape(s, quote=True)


def faq_de(a):
    """FAQ do artigo: o declarado em ARTICLES, ou o que já estava publicado."""
    return a.get("faq") or FAQ_PUBLICADO.get(a["slug"])


def faq_schema(a):
    """
    Bloco FAQPage separado, quando o artigo declara "faq".

    Fica em um <script> próprio de propósito: se o JSON do Article quebrar, o FAQ
    continua válido, e vice-versa. As perguntas precisam existir visíveis no corpo
    (o _bodies traz a mesma pergunta como H3), senão o Google desqualifica o rich result.
    """
    faq = faq_de(a)
    if not faq:
        return ""
    itens = ",\n".join(
        '      {{"@type": "Question", "name": {q}, "acceptedAnswer": {{"@type": "Answer", "text": {r}}}}}'.format(
            q=json.dumps(p, ensure_ascii=False), r=json.dumps(r, ensure_ascii=False))
        for p, r in faq)
    return ('\n  <script type="application/ld+json">\n'
            '  {\n    "@context": "https://schema.org",\n    "@type": "FAQPage",\n'
            '    "mainEntity": [\n' + itens + '\n    ]\n  }\n  </script>\n')


def faq_html(a):
    faq = faq_de(a)
    if not faq:
        return ""
    blocos = "".join(
        f'          <h3 id="faq-{i+1}">{esc(p)}</h3>\n          <p>{esc(r)}</p>\n'
        for i, (p, r) in enumerate(faq))
    return ('\n        <h2 id="faq">Perguntas frequentes</h2>\n' + blocos)


def build(a, idx):
    slug = a["slug"]; url = f"{BASE}/blog/{slug}.html"
    body = open(os.path.join(HERE, "_bodies", f"{slug}.body.html"), encoding="utf-8").read().strip()
    toc = list(a["toc"])
    # o bloco de fontes é injetado por _add_sources.py; reflete na TOC quando existir
    if faq_de(a) and not any(t["id"] == "faq" for t in toc):
        toc.append({"id": "faq", "label": "Perguntas frequentes"})
    if 'id="fontes"' in body and not any(t["id"] == "fontes" for t in toc):
        toc.append({"id": "fontes", "label": "Fontes"})
    toc_items = "\n".join(f'            <li><a href="#{t["id"]}">{esc(t["label"])}</a></li>' for t in toc)
    pills = a["heroPills"]
    faq_ld = faq_schema(a)
    faq_visivel = faq_html(a)
    # related: 3 outros artigos (rotativo entre os novos + 1 existente)
    others = [x["slug"] for x in ARTICLES if x["slug"] != slug]
    rel = others[idx % len(others):idx % len(others)+2] + ["crm-para-clinica-odontologica"]
    rel_items = ""
    for rs in rel:
        label = by_slug[rs]["title"] if rs in by_slug else EXISTING.get(rs, rs)
        rel_items += f'            <li><a href="/blog/{rs}.html">{esc(label)}</a></li>\n'
    schema = {
        "title": esc(a["title"]), "desc": esc(a["desc"]), "url": url, "slug": slug,
        "cat": esc(a["category"]),
    }
    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
{GTM}
{CLARITY}

  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(a.get("seoTitle", a["title"]))} — SaúdeCRM</title>
  <meta name="description" content="{esc(a["desc"])}">
  <meta property="og:title" content="{esc(a["title"])}">
  <meta property="og:description" content="{esc(a["desc"])}">
  <meta property="og:type" content="article">
  <meta property="og:locale" content="pt_BR">
  <meta property="og:site_name" content="SaúdeCRM">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{BASE}/og-blog.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Blog do SaúdeCRM: conteúdo prático para clínicas crescerem">
  <meta property="article:published_time" content="{DATE_ISO}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(a["title"])}">
  <meta name="twitter:description" content="{esc(a["desc"])}">
  <meta name="twitter:image" content="{BASE}/og-blog.jpg">
  <link rel="canonical" href="{url}">
  <link rel="icon" type="image/png" href="/favicon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{esc(a["title"])}",
    "description": "{esc(a["desc"])}",
    "image": {{
      "@type": "ImageObject",
      "url": "{BASE}/og-blog.jpg",
      "width": 1200,
      "height": 630
    }},
    "inLanguage": "pt-BR",
    "author": {{
      "@type": "Person",
      "@id": "{BASE}/sobre.html#juan-lourenco",
      "name": "Juan Lourenço",
      "url": "{BASE}/sobre.html",
      "jobTitle": "Fundador do SaúdeCRM",
      "description": "Acelerador de clínicas odontológicas. Trabalha dentro da operação, em agenda, recepção e funil de leads.",
      "sameAs": ["https://www.instagram.com/juansaraivalourenco/"]
    }},
    "publisher": {{ "@type": "Organization", "name": "SaúdeCRM", "legalName": "TDF Negócios Digitais LTDA", "url": "{BASE}/", "logo": {{ "@type": "ImageObject", "url": "{BASE}/logo.webp" }} }},
    "datePublished": "{DATE_ISO}",
    "dateModified": "{DATE_MODIFIED}",
    "url": "{url}",
    "mainEntityOfPage": {{ "@type": "WebPage", "@id": "{url}" }},
    "breadcrumb": {{
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{"@type": "ListItem", "position": 1, "name": "Home", "item": "{BASE}/"}},
        {{"@type": "ListItem", "position": 2, "name": "Blog", "item": "{BASE}/blog/"}},
        {{"@type": "ListItem", "position": 3, "name": "{esc(a["title"])}"}}
      ]
    }}
  }}
  </script>
{faq_ld}
  <style>{css}</style>
</head>
<body>

  <header>
    <div class="container">
      <div class="header-inner">
        <a href="/" class="logo">
          <img src="/logo.webp" alt="SaúdeCRM">
          <span class="logo-text">CRM <span>Saúde</span></span>
        </a>
        <a href="https://app.saudecrm.com/cadastro" class="btn-cta">Começar grátis →</a>
      </div>
    </div>
  </header>

  <div class="container">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="/">Home</a>
      <span class="breadcrumb-sep">›</span>
      <a href="/blog/">Blog</a>
      <span class="breadcrumb-sep">›</span>
      <span class="breadcrumb-current">{esc(a["title"])}</span>
    </nav>

    <a href="/blog/" class="back-link">← Voltar ao Blog</a>

    <div class="article-wrap">
      <main>
        <div class="article-header">
          <span class="post-category">{esc(a["category"])}</span>
          <h1>{esc(a["title"])}</h1>
          <div class="article-meta">
            <span>{DATE_HUMAN}</span>
            <span class="article-meta-sep">·</span>
            <span>{a["readTime"]} min de leitura</span>
            <span class="article-meta-sep">·</span>
            <span>Por <a href="/sobre.html" rel="author" style="color:inherit;text-decoration:underline;text-underline-offset:2px">Juan Lourenço</a></span>
            <span class="article-meta-sep">·</span>
            <span>Atualizado em {DATE_MODIFIED_HUMAN}</span>
          </div>
        </div>

        <div class="article-hero-visual">
          <div class="hero-pills">
            <div class="hero-pill">{esc(pills[0])}</div>
            <div class="hero-pill-main">{esc(pills[1])}</div>
            <div class="hero-pill">{esc(pills[2])}</div>
          </div>
        </div>

        <article class="article-content">
{body}{faq_visivel}
        </article>

        <div class="author-box" style="display:flex;gap:18px;align-items:flex-start;background:#fff;border:1px solid #E3E8F2;border-radius:14px;padding:22px 24px;margin:34px 0 8px">
          <img src="/logo.webp" alt="Juan Lourenço" width="56" height="56" style="width:56px;height:56px;border-radius:50%;object-fit:cover;flex:none">
          <div style="font-size:15px;line-height:1.6">
            <div style="font-family:'Plus Jakarta Sans',sans-serif;font-weight:800;font-size:16px;margin-bottom:2px">Juan Lourenço</div>
            <div style="font-size:13px;color:#5A6472;margin-bottom:10px">Fundador do SaúdeCRM · acelerador de clínicas odontológicas</div>
            <p style="margin:0 0 10px;color:#232B39">Trabalha dentro da operação de clínicas: agenda, recepção, funil de leads e fechamento de tratamento. Escreve a partir do que vê se repetir em clínicas diferentes, não de teoria.</p>
            <p style="margin:0;color:#232B39"><a href="/sobre.html" rel="author">Sobre o autor</a> · <a href="https://www.instagram.com/juansaraivalourenco/" rel="me nofollow">@juansaraivalourenco</a></p>
          </div>
        </div>
      </main>

      <aside class="sidebar">
        <div class="sidebar-card">
          <h4>Neste artigo</h4>
          <ul class="toc-list">
{toc_items}
          </ul>
        </div>

        <div class="sidebar-cta">
          <h4>SaúdeCRM</h4>
          <p>CRM com WhatsApp integrado para clínicas. Teste grátis por 7 dias.</p>
          <a href="https://app.saudecrm.com/cadastro">Começar grátis →</a>
        </div>

        <div class="sidebar-card" style="margin-top:20px;">
          <h4>Mais do blog</h4>
          <ul class="toc-list">
{rel_items}          </ul>
        </div>
      </aside>
    </div>
  </div>

  <footer>
    <div class="container">
      <div class="footer-inner">
        <p class="footer-copy">© 2026 SaúdeCRM. Todos os direitos reservados.</p>
        <div class="footer-links">
          <a href="/">Início</a>
          <a href="/blog/">Blog</a>
          <a href="/sobre.html">Sobre</a>
          <a href="https://app.saudecrm.com/cadastro">Começar grátis</a>
        </div>
      </div>
    </div>
  </footer>

</body>
</html>'''

for i, a in enumerate(ARTICLES):
    out = build(a, i)
    with open(os.path.join(OUT, f'{a["slug"]}.html'), "w", encoding="utf-8") as f:
        f.write(out)
    print(f'OK {a["slug"]}.html ({len(out)} bytes)')
print("Total:", len(ARTICLES), "artigos gerados")
