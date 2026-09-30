# Story 007: CTA único para diagnóstico

Status: Done

## Controle do documento

Autoria: Juan Lourenço. Versão: 1.0. Data: 30/09/2026.

## Briefing

A LP deve conduzir exclusivamente ao formulário de diagnóstico. O acesso de login não deve aparecer na navegação principal ou no menu mobile.

## IN

- Remover links de login da LP principal.
- Manter o CTA de cabeçalho apontando para `#diagnostico`.
- Preservar a captura de origem para o formulário.

## OUT

- Alterar a LP arquivada em `/lp-v1`, o aplicativo, o contrato do formulário ou páginas legais.

## Critérios de aceite

1. Nenhum link para `app.saudecrm.com` existe na LP principal.
2. O CTA de cabeçalho leva ao formulário.
3. Navegação desktop e mobile seguem acessíveis.
4. Testes, lint, typecheck, build e verificação no domínio público passam.

## Validação

- Produção confirmada na publicação `dpl_4m81deaU1Fd8Goj71RkNWiTqnc3g`.
- A página pública não contém links para `app.saudecrm.com` nem rótulos de login.
- Cinco links internos direcionam para `#diagnostico`, incluindo cabeçalho e menu mobile.
- Testes, lint, typecheck e build aprovados.
