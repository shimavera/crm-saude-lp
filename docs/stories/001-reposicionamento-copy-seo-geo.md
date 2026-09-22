# Story 001: Reposicionamento da LP e expansão SEO/GEO

**Status:** Ready
**Tipo:** Marketing e conteúdo

## Contexto

A LP do SaúdeCRM estava concentrando a promessa em crescimento genérico e IA no WhatsApp. A
nova narrativa posiciona o produto como CRM para clínicas, conectando aquisição, atendimento,
funil, follow-up e acompanhamento de resultados.

## Escopo

**IN**

- revisar hero, metadados, CTA, simulação e funcionalidades da home
- publicar três artigos orientados a SEO e GEO
- incluir FAQ, resposta direta, links internos e sitemap para os novos artigos
- preservar o padrão estático e o gerador existente do blog

**OUT**

- alterar o aplicativo autenticado
- alterar preços ou condições comerciais sem validação da oferta vigente
- publicar depoimentos, logos ou números sem comprovação

## Critérios de aceite

- **AC1** - A home apresenta o SaúdeCRM como CRM para clínicas e não apenas como IA de WhatsApp.
- **AC2** - A primeira dobra explica o problema entre anúncio, WhatsApp e agendamento.
- **AC3** - A simulação informa que seus resultados são ilustrativos.
- **AC4** - Existem três novos artigos com resposta objetiva, FAQ e links internos.
- **AC5** - Os três artigos estão no índice do blog, no `sitemap.xml` e no `llms.txt`.
- **AC6** - JSON-LD e links internos passam a validação local.

## Validação

- `python3 .blog-build/_build.py`
- `python3 .blog-build/_links_internos.py`
- `python3 .blog-build/_gen_sitemap.py`
- validação local de JSON-LD e links internos
- `git diff --check`
