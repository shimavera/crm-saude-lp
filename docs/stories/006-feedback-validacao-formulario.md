# Story 006: feedback de validação do diagnóstico

Status: Done

## Controle do documento

Autoria: Juan Lourenço. Versão: 1.0. Data: 29/09/2026.

## Briefing

Um envio em produção retornou HTTP 400. A interface mostrou uma mensagem de indisponibilidade, embora a requisição tenha sido recusada por validação antes do encaminhamento à planilha.

## IN

- Exibir orientação específica para cada erro de validação devolvido pela API.
- Alinhar a validação de WhatsApp no navegador à regra já usada pelo servidor.
- Manter os campos preenchidos, foco no campo inválido e mensagem temporária apenas para falhas de entrega.
- Cobrir os códigos de validação no teste da API.

## OUT

- Alterar dados enviados, destino da planilha, regras de consentimento ou a estética aprovada.

## Critérios de aceite

1. Respostas HTTP 400 nunca exibem a mensagem de indisponibilidade.
2. WhatsApp inválido é bloqueado antes da requisição e explica o ajuste necessário.
3. Campos recusados pela API recebem foco e mensagem compreensível.
4. Erro de serviço continua preservando os dados e permite nova tentativa.
5. Testes, lint, typecheck, build e validação no domínio público passam.

## Validação

- Registro da falha real: HTTP 400 em `POST /api/diagnostic`, portanto recusada antes do serviço de planilha.
- Requisição de QA com dados fictícios confirmou o fluxo completo com HTTP 200 em 13,4 segundos.
- Browser no domínio público confirmou que WhatsApp inválido é bloqueado no campo, sem requisição e sem a mensagem de indisponibilidade.
- Testes, lint, typecheck e build aprovados.
