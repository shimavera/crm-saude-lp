# Story 004: telas reais com dados demonstrativos e copy de IA

Status: Validated in preview

## Controle do documento

Autoria: Juan Lourenço. Versão: 1.0. Atualização: 29/09/2026.
Histórico: versão 1.0, briefing e critérios da segunda rodada da LP.

## Briefing

Preservar a estética futurista aprovada na Story 003. Tornar os benefícios da IA claros para gestores e equipes de clínicas sem conhecimento técnico. Usar as telas fornecidas como referência visual do produto, recriando as interfaces com dados demonstrativos.

Fonte dos recursos: declaração direta do usuário nesta rodada. IA disponível 24 horas, compreensão e envio de áudio, compreensão de imagem, qualificação, condução ao agendamento com profissional, metodologia SPIN Selling, sequência de follow-up, apoio à recepção, conhecimento da clínica e refinamento com o tempo. A redação não transforma esses recursos em garantia de resultado.

## História do usuário

Como gestor de clínica, quero enxergar o produto e entender como a IA atende, retoma conversas e conduz o paciente ao agendamento, para avaliar seu uso na rotina da recepção.

## IN

- Manter composição, paleta, tipografia, atmosfera, animações e responsividade aprovadas.
- Copy final por seção conforme `docs/marketing/lp-futurista-copy-v2.md`.
- Explicar áudio, imagem, atendimento 24 horas, qualificação, agendamento e retomada de conversas com exemplos concretos.
- SPIN em linguagem simples: compreender situação, necessidade, impacto na rotina e valor do próximo passo antes do convite ao agendamento.
- Interfaces visualmente fiéis às telas fornecidas, usando exclusivamente dados demonstrativos criados para a LP. Técnica definida pela implementação.
- Demonstrações de áudio, imagem, agendamento e sequência de retomada com identificação visível de exemplo.
- Handoff explicado como encaminhamento para a equipe, com histórico.
- Refinamento da IA por informações e ajustes da equipe ao longo do tempo.
- Preservar o diagnóstico como conversão principal, contrato do formulário, SEO, analytics, links legais e blog.

## OUT

- Reestilizar a direção visual aprovada ou alterar a identidade.
- Publicar screenshots brutas fornecidas pelo usuário.
- Expor nomes, telefones, e-mails, fotos, mensagens, links identificáveis ou faturamento reais.
- Implementar recursos novos no CRM, áudio clínico real ou integrações sem evidência.
- Afirmar diagnóstico clínico por imagem, recomendação de tratamento, aprendizado automático ilimitado ou memória de pacientes.
- Inventar resultados financeiros, taxas de conversão, clientes, depoimentos ou eficácia clínica.
- Garantir agendamento, fechamento, conversão, ausência de falhas ou disponibilidade percentual.

## Critérios de aceite

1. Hero preserva o título aprovado e explicita IA 24 horas, mensagens de texto, áudio, imagens e agendamento no subtítulo.
2. Cada benefício descreve uma situação da rotina da clínica e o recurso que a apoia, sem jargão desnecessário.
3. A primeira menção de follow-up traduz o termo como retomar conversas em sequência e no momento certo.
4. SPIN é explicado como compreensão da situação, da necessidade, do impacto e do valor do próximo passo; não é apresentado como manipulação nem como consulta clínica.
5. Áudio e imagem possuem exemplos visuais legíveis; áudio só possui controle de reprodução se houver mídia real demonstrativa. Não simular um player funcional sem arquivo.
6. Imagem é recurso de compreensão do que o paciente compartilha, sem sugerir diagnóstico, avaliação de sintomas ou indicação de tratamento.
7. Agendamento menciona o profissional e as regras configuradas, sem inventar integração de calendário específica ou disponibilidade real.
8. Sequência de retomada apresenta mensagens e intervalos identificados como exemplo, sujeitos a regras, consentimento e configuração da clínica; não fixar um comportamento universal.
9. Texto diferencia a conversa contextual de um fluxo limitado a menus rígidos, sem desqualificar concorrentes ou prometer entendimento perfeito.
10. Refinamento da IA depende das informações e ajustes da equipe ao longo do tempo; encaminhamento humano e acompanhamento das conversas permanecem claros.
11. Interfaces seguem visualmente as referências reais, mas todo dado exibido é demonstrativo, inclusive nomes de profissional, conversas, agendas, indicadores e valores. Nenhuma screenshot bruta entra em assets.
12. Todo mock visível informa que é demonstração com dados fictícios. Não usar o mock como prova de resultado comercial.
13. Diagnóstico continua como CTA principal. Botões demonstrativos levam a estados reais da demonstração.
14. Validar leitura e ausência de overflow em desktop e mobile; cliques, teclado, pausa e movimento reduzido continuam funcionando.
15. Rodar testes, lint, typecheck, build e revisão no navegador após implementação. Não declarar publicação em produção nem persistência do formulário sem prova própria dessas etapas.

## Limite desta entrega documental

Esta rodada inicial produz briefing, story Ready e copy. HTML, CSS e JavaScript serão alterados apenas após coordenação do responsável pela implementação.

## Implementação

- Copy v2 integrada ao HTML, mantendo título do hero e estética aprovada.
- Hero usa dashboard demonstrativo claro; galeria Dashboard, Conversas e Kanban usa arquivos JPG em `assets/product/`.
- Abas navegáveis por teclado e dialog nativo com Escape e retorno de foco.
- Exemplos de áudio transcrito, imagem, agendamento e encaminhamento humano. Nenhum player de áudio falso.
- Seções de SPIN em linguagem simples, sequência configurável de retomadas e refinamento orientado pela equipe.
- Formulário HTML comparado com a versão anterior e preservado integralmente. API não alterada.

## Validação técnica desta etapa

- Sintaxe JavaScript, testes 6/6, lint e typecheck aprovados.
- IDs únicos, âncoras locais válidas e imagens com alt verificados.
- Build final e revisão visual dependem dos três assets de produto gerados em paralelo.
- Não houve publicação nesta etapa.


## Validação final da prévia

- Testes automatizados: 6 aprovados; lint, typecheck, build e `git diff --check` aprovados.
- Browser local: desktop 1280 px, mobile 390 e 320 px sem overflow; imagens carregadas; tabs por clique e teclado; modal amplia a imagem, aceita Escape e devolve o foco; rolagem horizontal mobile e dica de navegação visíveis.
- Cenas de imagem e agendamento, menu por Escape e preferência de movimento reduzido verificados.
- Browser remoto: copy, capturas com dados fictícios, modal Kanban, Clarity, meta Search Console e canonical confirmados.
- Arquivos remotos da home, CSS, JavaScript, configuração e três capturas correspondem byte a byte aos arquivos locais. Harness de documentação retorna 404 na prévia pública.
- Formulário: POST inválido retorna 400; nenhum lead real foi enviado nesta rodada.
- Capturas são reconstruções estáticas baseadas nas referências fornecidas, com dados sintéticos. Não são screenshots de produção nem execução dos componentes atuais do CRM.
- Prévia autenticada: https://crm-saude-e9em543lk-juanlourenco.vercel.app . Link de avaliação específico compartilhado separadamente, com validade de 23 horas.
- Produção não foi alterada. Persistência real de lead na planilha continua sem verificação nesta entrega.
