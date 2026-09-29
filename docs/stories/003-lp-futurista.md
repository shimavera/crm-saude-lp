# Story 003: LP futurista

Status: Validated in preview

Como gestor de clínica, quero entender como a IA apoia atendimento e follow-up e solicitar avaliação da operação.

## IN
Hero, demonstração interativa ilustrativa, narrativa de produto, FAQ, formulário existente, visual responsivo e animações acessíveis. SEO e atribuição preservados. Proxy same-origin /api/diagnostic encaminha o contrato existente para LEAD_WEBHOOK_URL com confirmação verificável.

## OUT
Backend do CRM, automação real de atendimento, alterações no blog e páginas legais, métricas e integrações não comprovadas.

## Critérios de aceite
1. Visual original preto/azul com hero cinematográfico e animações reais.
2. CTA de demonstração funcional e estados interativos acessíveis por teclado.
3. Formulário mantém destino via proxy, campos, atribuição, consentimento e feedback sem alegar persistência não observada.
4. Sem overflow mobile, conteúdo legível e controles acessíveis.
5. Reduced motion, pausa manual, suspensão de canvas em aba oculta.
6. Links legais e blog preservados; schema sem preço não exibido.
7. Testes, lint, typecheck e validação browser executados pela revisão.

## Validação

- Preview publicada validada no navegador; analytics e metadados carregados.
- Layout desktop em 1280 px e mobile em 390 px revisados.
- Demonstração testada por clique e teclado; FAQ funcional.
- Preferência de movimento reduzido e pausa manual verificadas.
- Telefone com máscara aceito; falha local preserva os dados preenchidos.
- Testes, lint, typecheck e build executados com sucesso pela revisão de entrega.

## Pendências de entrega

- Publicação e validação no domínio de produção.
- Confirmação de persistência de uma solicitação no destino final da planilha.

A validação da preview e a confirmação de encaminhamento da API não representam prova de persistência na planilha.
