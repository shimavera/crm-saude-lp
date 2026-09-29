# Story 005: diagnóstico em duas etapas e publicação da LP

Status: Ready for production; live verification pending

## Controle do documento

Autoria: Juan Lourenço. Versão: 1.0. Data: 29/09/2026.
Histórico: versão 1.0, redesenho aprovado pelo usuário e preparação para publicação.

## Briefing

O usuário aprovou a nova LP e solicitou melhorar o formulário, publicar a nova experiência no domínio principal e preservar a versão anterior em /lp-v1. O formulário deve parecer parte da experiência futurista, com escolhas rápidas e contato em uma segunda etapa.

## IN

- Duas etapas: Sua clínica e Vamos conversar.
- Três perguntas com escolhas em grupos de radio, seguidas de nome, WhatsApp, e-mail e consentimento.
- Progresso discreto, navegação avançar/voltar, respostas preservadas e validação por etapa.
- Sem JavaScript, todos os campos ficam visíveis e o formulário continua com POST para a API.
- Preservar os valores do payload, endpoint, consentimento, atribuição, honeypot e confirmação por resposta verificável.
- Publicar a nova LP na raiz e preservar a anterior em /lp-v1, sob responsabilidade da entrega.

## OUT

- Alterações na API de diagnóstico ou no contrato de dados.
- Terceira etapa, novo funil comercial, métricas ou condições de oferta inventadas.
- Mudanças na estética aprovada, galeria, copy principal, blog ou páginas legais.

## Critérios de aceite

1. Formulário elegante e leve, alinhado ao preto/azul, com fieldsets e legendas acessíveis.
2. Etapa 1 valida as três escolhas antes de avançar; erro aparece junto da pergunta.
3. Etapa 2 possui campos de contato, consentimento e envio real; voltar mantém os valores e as escolhas.
4. Teclado, foco visível, seleção nativa de radio, leitor de tela e movimento reduzido funcionam.
5. Mobile usa texto legível, inputs de 16 px e alvos de pelo menos 44 px; sem overflow ou saltos de layout ao trocar etapa.
6. Fallback sem JavaScript exibe todas as perguntas e usa POST, sem dados pessoais na URL.
7. Payload e opções mantêm exatamente os valores anteriores; erro preserva o preenchimento e sucesso exige response.ok e JSON ok true.
8. Testes, lint, typecheck, build e revisão browser passam antes de publicar.
9. Entrega valida a nova página no domínio de produção e a LP anterior em /lp-v1, sem declarar persistência do lead sem prova do destino.

## Evidências técnicas

- Formulário redesenhado com fieldsets, opções radio e duas etapas.
- Comparação automatizada confirmou os mesmos valores de volume, equipe e necessidade dos selects anteriores.
- Validação inline, navegação com respostas preservadas, reserva de altura e fallback sem JavaScript implementados.
- Testes 6/6, lint, typecheck e build aprovados.
- Revisão visual, publicação em produção e preservação da LP anterior ainda dependem da etapa de entrega.

## Validação antes da publicação

- Browser local: etapas do formulário, validação das três respostas, foco no título da etapa, retorno preservando campos, consentimento obrigatório e erro de envio honesto validados.
- Desktop 1280 px e mobile 390/320 px sem overflow.
- Versão anterior preservada a partir de resposta LIVE de saudecrm.com, não de uma versão presumida do Git. Manifesto em `docs/lp-v1-preservation.json`.
- `/lp-v1/` validada visualmente, sem imagens quebradas, com noindex e canonical próprio. Recursos isolados e formulário compatível com o proxy confirmado.
- 8 testes, lint, typecheck e build aprovados. Preview valida home e arquivo com bytes iguais aos arquivos locais.
- Variáveis de produção preparadas; publicação e validação real de captura serão registradas após o deploy.

## Correção encontrada na validação em produção

Um envio de QA foi persistido na planilha, mas a interface recebeu HTTP 502 de confirmação não concluída. O proxy tinha limite de 12 segundos e o navegador de 20 segundos. Os logs existentes confirmam o status, mas não registravam a duração; timeout é a hipótese principal, não uma causa comprovada.

A correção amplia a janela do destino para 30 segundos, da função para 60 segundos e do navegador para 45 segundos. Logs de falha passam a incluir apenas categoria, duração e status HTTP, sem dados pessoais, corpo de resposta ou endpoint. Não repetir o marcador já persistido. O aceite exige novo teste com marcador distinto e confirmação na interface e na planilha.
