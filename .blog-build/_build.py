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
    # ── Publicados em 15/08/2026. "crm-para-dentistas" nasceu do Search Console:
    #    era a consulta com mais impressões e não existia página dedicada.
    {
        "slug": "crm-para-dentistas",
        "title": "CRM para Dentistas: O Que É, Para Que Serve e Quando Vale a Pena",
        "seoTitle": "CRM para Dentistas: Guia Completo",
        "desc": "CRM para dentistas: o que faz na rotina do consultório, a diferença para o software de gestão, quanto custa, quando passa a valer a pena e como implantar.",
        "category": "Guia Completo",
        "readTime": 7,
        "heroPills": ["CRM odontológico", "WhatsApp do consultório", "Orçamento que não some"],
        "toc": [{"id":"o-que-e","label":"O que é"},{"id":"por-que-dentista-precisa","label":"Por que precisa"},{"id":"o-que-faz-na-pratica","label":"O que faz na prática"},{"id":"crm-x-software-gestao","label":"CRM x software de gestão"},{"id":"quando-precisa","label":"Quando passa a precisar"},{"id":"quanto-custa","label":"Quanto custa"},{"id":"como-escolher","label":"Como escolher"},{"id":"implementacao","label":"Como implantar"},{"id":"conclusao","label":"Conclusão"}],
        "faq": [
            ("O que é um CRM para dentistas?",
             "É o sistema que organiza tudo o que acontece antes do paciente sentar na cadeira: a mensagem no WhatsApp, a dúvida sobre valor, o orçamento enviado, o retorno de quem sumiu e o agendamento da avaliação. O prontuário e o plano de tratamento continuam no software de gestão; o CRM cuida da conversa que leva o paciente até lá."),
            ("Qual a diferença entre CRM e software de gestão odontológica?",
             "O software de gestão cuida de quem já é paciente: prontuário, odontograma, evolução, agenda clínica e faturamento. O CRM cuida de quem ainda não é: lead, orçamento, follow-up e conversão. Consultório que só tem gestão perde paciente antes do cadastro."),
            ("Quanto custa um CRM para dentistas?",
             "Entre cerca de R$ 100 e R$ 700 por mês no Brasil em 2026. A unidade de cobrança pesa mais que o valor: alguns sistemas cobram por dentista, o que encarece conforme a equipe cresce, e outros cobram por clínica com limite de contatos. Num consultório com ticket de alguns milhares de reais, costuma bastar um paciente recuperado por trimestre para pagar a mensalidade."),
            ("Consultório pequeno precisa de CRM?",
             "Só quando os pacientes deixam de chegar apenas por indicação. Enquanto o volume é baixo e você mesmo responde todas as mensagens, não precisa. A partir do momento em que há anúncio rodando, perfil ativo nas redes ou duas pessoas respondendo o mesmo número, existe um estágio anterior ao cadastro que ninguém está controlando."),
        ],
    },
    {
        "slug": "precificacao-consulta-clinica-medica",
        "title": "Precificação de Consulta em Clínica Médica: Como Calcular Quanto Cobrar",
        "seoTitle": "Quanto Cobrar por Consulta em Clínica Médica",
        "desc": "Como calcular o preço da consulta particular: custo fixo por atendimento, custos esquecidos, capacidade realista, posicionamento, convênio e quando reajustar.",
        "category": "Financeiro",
        "readTime": 8,
        "heroPills": ["Preço da consulta", "Custo por hora", "Margem real"],
        "toc": [{"id":"como-calcular","label":"Como calcular"},{"id":"custo-fixo","label":"O que entra no custo fixo"},{"id":"custo-esquecido","label":"Custos esquecidos"},{"id":"quantas-consultas","label":"Capacidade realista"},{"id":"posicionamento","label":"Posicionamento"},{"id":"convenio","label":"E o convênio?"},{"id":"reajuste","label":"Quando reajustar"},{"id":"conclusao","label":"Conclusão"}],
        "faq": [
            ("Como calcular o preço de uma consulta particular?",
             "Divida o custo fixo mensal da clínica pelo número realista de consultas por mês, some o custo variável por atendimento e aplique a margem desejada. O resultado é o preço mínimo, abaixo do qual atender dá prejuízo. Só depois disso entra a comparação com o mercado, para decidir onde se posicionar acima desse piso."),
            ("O que entra no custo fixo de um consultório?",
             "Aluguel e condomínio, energia, água e internet, salários e encargos da equipe administrativa, contabilidade, sistemas e software, seguro, taxas de conselho, limpeza, manutenção e a depreciação de equipamentos e mobiliário dividida pela vida útil em meses. O pró-labore de quem administra também deve entrar."),
            ("Por que o no-show muda o preço da consulta?",
             "Porque ele reduz o denominador da conta. Se você planeja 120 consultas por mês e 15 faltam, o custo fixo passa a se dividir por 105, e o preço mínimo real sobe quase 15%. Numa clínica com 12% de falta, reduzir o no-show pela metade tem efeito parecido com um reajuste de 6% na tabela, sem desgaste com o paciente."),
            ("Quando reajustar o valor da consulta?",
             "Refaça a conta de custo por hora a cada seis meses e reajuste em data definida e comunicada com antecedência, quando o custo fixo subir, quando o tempo de consulta aumentar ou quando a demanda estiver consistentemente acima da capacidade. Fila de espera longa é o sinal mais claro de que o preço está abaixo do que o mercado aceita pagar."),
        ],
    },
    {
        "slug": "precificacao-procedimentos-esteticos",
        "title": "Precificação de Procedimentos Estéticos: Como Calcular Sem Perder Margem",
        "seoTitle": "Como Precificar Procedimentos Estéticos",
        "desc": "Como precificar procedimento estético: custo da hora de sala, depreciação de equipamento, pacotes e protocolos, comparação de preço no Instagram e promoções.",
        "category": "Financeiro",
        "readTime": 8,
        "heroPills": ["Hora de sala", "Margem por sessão", "Pacotes e protocolos"],
        "toc": [{"id":"como-calcular","label":"Como calcular"},{"id":"hora-de-sala","label":"Custo da hora de sala"},{"id":"equipamento","label":"Equipamento caro"},{"id":"pacotes","label":"Pacotes e protocolos"},{"id":"comparacao","label":"Comparação de preço"},{"id":"promocao","label":"Promoção destrói margem?"},{"id":"reajuste","label":"Revisão da tabela"},{"id":"conclusao","label":"Conclusão"}],
        "faq": [
            ("Como calcular o preço de um procedimento estético?",
             "Some o custo do insumo usado naquela sessão, o custo da hora de sala multiplicado pela duração do procedimento e o custo do profissional que executa; depois aplique a margem desejada. O insumo costuma ser a menor parte: um procedimento de 40 minutos numa sala que custa R$ 180 por hora já carrega R$ 120 de estrutura antes de qualquer produto."),
            ("Como calcular a hora de sala de uma clínica de estética?",
             "Some todo o custo fixo mensal (aluguel, energia, equipe de apoio, sistemas, marketing e depreciação dos equipamentos) e divida pelas horas realmente disponíveis de atendimento, não pelas horas do calendário. Uma sala aberta 8 horas por dia em 22 dias tem 176 horas nominais, mas a ocupação real dificilmente passa de 60% a 70%."),
            ("Como precificar pacotes de procedimentos?",
             "Multiplique o custo de cada sessão pelo número de sessões e aplique a margem sobre o total, reduzindo apenas o que de fato barateia com a repetição: o custo de captação, já pago uma vez, e eventuais ganhos de escala no insumo. Dar 30% de desconto porque o cliente compra mais ignora que a estrutura continua custando o mesmo por sessão."),
            ("Dar desconto em procedimento estético compensa?",
             "Raramente, quando o desconto é dado sobre o preço final sem refazer a conta. Um procedimento com 30% de margem que recebe 20% de desconto não perde 20% do lucro: perde dois terços dele. Antes de qualquer campanha, calcule quantas sessões a mais ela precisa gerar só para empatar com o faturamento anterior."),
        ],
    },
    {
        "slug": "gestao-de-clinicas-guia",
        "title": "Gestão de Clínicas: As 6 Frentes que Definem o Resultado do Mês",
        "seoTitle": "Gestão de Clínicas: Guia Prático",
        "desc": "Guia de gestão de clínicas: as 6 frentes (captação, conversão, agenda, equipe, finanças e retenção), o que medir em cada uma, por onde começar e erros comuns.",
        "category": "Gestão de Clínica",
        "readTime": 8,
        "heroPills": ["6 frentes de gestão", "Indicadores por área", "Decisão com número"],
        "toc": [{"id":"o-que-e","label":"O que é na prática"},{"id":"por-onde-comecar","label":"Por onde começar"},{"id":"agenda","label":"Buracos na agenda"},{"id":"financeiro","label":"Além do faturamento"},{"id":"equipe","label":"Equipe sem inchar a folha"},{"id":"processos","label":"Processos essenciais"},{"id":"rotina","label":"Rotina de gestão"},{"id":"erros","label":"Erros comuns"},{"id":"conclusao","label":"Conclusão"}],
        "faq": [
            ("O que é gestão de clínica na prática?",
             "É cuidar de seis frentes ao mesmo tempo: captação, conversão, agenda e operação, equipe, finanças e retenção. Cada uma tem indicador próprio e cada uma pode ser o gargalo do mês. Gerir é descobrir qual delas está segurando o resultado agora e agir só ali, em vez de tentar melhorar tudo ao mesmo tempo."),
            ("Por onde começar a organizar a gestão da clínica?",
             "Pela conversão, não pela captação. Antes de investir mais em anúncio, meça quantos contatos já chegam e quantos se perdem no caminho: é comum descobrir que metade dos interessados some por demora de resposta, o que significa que dobrar o investimento em mídia dobraria o desperdício. A ordem que funciona é conversão, agenda, retenção e só então captação."),
            ("Quais indicadores toda clínica deveria acompanhar?",
             "Leads por mês e custo por lead na captação; taxa de lead para avaliação e de avaliação para fechamento na conversão; taxa de ocupação e taxa de falta na agenda; produção por profissional na equipe; margem por procedimento e fluxo de caixa nas finanças; taxa de retorno e tempo médio entre visitas na retenção."),
            ("Qual rotina de gestão manter numa clínica?",
             "Uma reunião semanal de 30 minutos olhando quatro números (contatos recebidos, agendamentos, faltas e fechamentos) e uma revisão mensal mais longa com o financeiro. O que faz diferença não é a profundidade da análise, é a constância: número olhado toda semana revela tendência antes de virar problema."),
        ],
    },
    {
        "slug": "equipe-minima-para-clinica",
        "title": "Equipe Mínima para Clínica: Quem Contratar e em Que Ordem",
        "seoTitle": "Equipe Mínima para Clínica: Guia Prático",
        "desc": "Qual a equipe mínima de uma clínica por porte, como saber se falta gente ou falta processo, o custo real de uma contratação e a ordem certa de contratar.",
        "category": "Gestão de Clínica",
        "readTime": 7,
        "heroPills": ["Equipe por porte", "Custo real da contratação", "Ordem de contratar"],
        "toc": [{"id":"equipe-minima","label":"Qual é a equipe mínima"},{"id":"sobrecarga-ou-desorganizacao","label":"Sobrecarga ou desorganização"},{"id":"custo-real","label":"Custo real da contratação"},{"id":"o-que-nao-terceirizar","label":"O que fica interno"},{"id":"ordem-de-contratacao","label":"Ordem de contratação"},{"id":"funcoes-acumuladas","label":"O que o dono deve largar"},{"id":"produtividade","label":"Equipe bem dimensionada"},{"id":"conclusao","label":"Conclusão"}],
        "faq": [
            ("Qual é a equipe mínima de uma clínica?",
             "Três funções, que nem sempre são três pessoas: quem atende clinicamente, quem cuida da recepção e do agendamento, e quem responde pela gestão e pelo financeiro. Num consultório iniciante, o profissional acumula a terceira função e a recepção é uma pessoa só."),
            ("Como saber se preciso contratar ou apenas organizar processo?",
             "Anote por três dias em que a recepção gasta o tempo. Se a maior parte for atendimento presencial, acolhimento e negociação com paciente, falta gente. Se a maior parte for tarefa repetitiva, como responder as mesmas perguntas, confirmar consulta uma a uma e procurar histórico, o problema é processo, e contratar apenas divide a bagunça em duas."),
            ("Quanto custa de verdade contratar para a clínica?",
             "Bem mais que o salário: somam-se encargos, provisão de férias e décimo terceiro, benefícios, exame admissional, uniforme, o tempo de quem treina, os primeiros meses de produtividade parcial e o risco de rotatividade, que devolve a clínica ao ponto de partida e leva junto o conhecimento acumulado."),
            ("Em que ordem contratar conforme a clínica cresce?",
             "Primeiro a recepção integral, quando o profissional passa a responder mensagem entre atendimentos. Depois o apoio clínico, quando preparo e limpeza limitam o número de atendimentos. Depois alguém dedicado ao comercial e follow-up, quando há orçamento parado acumulando. Coordenação só quando já existem processos escritos e mais de uma pessoa por função."),
        ],
    },
    {
        "slug": "crm-ou-planilha-para-clinica",
        "title": "CRM ou Planilha para Clínica: Qual Escolher?",
        "seoTitle": "CRM ou Planilha para Clínica: Qual Escolher?",
        "desc": "CRM ou planilha para clínica: entenda quando a planilha ainda resolve, quando ela começa a esconder oportunidades e como escolher um CRM sem complicar a operação.",
        "category": "Gestão de Clínica",
        "readTime": 6,
        "heroPills": ["CRM para clínicas", "Organização de leads", "Processo comercial"],
        "toc": [{"id":"resposta-curta","label":"Resposta curta"},{"id":"quando-planilha-resolve","label":"Quando a planilha resolve"},{"id":"sinais-de-limite","label":"Sinais de limite"},{"id":"o-que-crm-organiza","label":"O que o CRM organiza"},{"id":"como-migrar","label":"Como migrar"},{"id":"conclusao","label":"Conclusão"}],
        "faq": [
            ("Quando uma clínica deve trocar a planilha por um CRM?", "Quando a equipe já não consegue responder quem está sem retorno, quando mais de uma pessoa atende os mesmos contatos ou quando a clínica investe em anúncios e não consegue ligar o lead ao resultado. O problema não é a quantidade de linhas: é a falta de próximo passo."),
            ("Planilha é suficiente para poucos leads?", "Pode ser, se uma pessoa acompanha todos os contatos e o volume é baixo. A planilha deixa de funcionar quando exige atualização manual constante, não avisa tarefas atrasadas ou vira uma versão diferente em cada computador."),
            ("CRM substitui o software de gestão da clínica?", "Não. O software de gestão cuida do paciente já cadastrado, com agenda, prontuário e financeiro. O CRM cuida da jornada anterior, desde o primeiro contato até o agendamento e o fechamento."),
            ("Como escolher um CRM sem complicar a equipe?", "Comece pelo problema mais caro: lead sem resposta, orçamento sem retorno ou falta de atribuição. Escolha uma ferramenta que a recepção consiga usar no fluxo real, teste com dados da operação e só depois ative recursos avançados."),
        ],
    },
    {
        "slug": "como-saber-qual-anuncio-trouxe-paciente",
        "title": "Como Saber Qual Anúncio Trouxe Cada Paciente para a Clínica",
        "seoTitle": "Como Saber Qual Anúncio Trouxe Cada Paciente",
        "desc": "Aprenda a acompanhar a origem dos leads e descobrir quais campanhas, anúncios e canais realmente geram pacientes para a sua clínica.",
        "category": "Marketing Digital",
        "readTime": 7,
        "heroPills": ["Atribuição de leads", "Google Ads e Meta Ads", "Marketing de clínicas"],
        "toc": [{"id":"resposta-curta","label":"Resposta curta"},{"id":"por-que-nao-basta-contar-leads","label":"Por que contar leads não basta"},{"id":"o-que-registrar","label":"O que registrar"},{"id":"do-clique-ao-paciente","label":"Do clique ao paciente"},{"id":"indicadores","label":"Indicadores"},{"id":"conclusao","label":"Conclusão"}],
        "faq": [
            ("Como descobrir de onde veio um paciente?", "Registre a origem no primeiro contato e preserve campanha, anúncio, página e canal junto do lead. Depois compare essa origem com as etapas do funil, como agendamento, comparecimento e tratamento fechado."),
            ("Qual a diferença entre custo por lead e custo por paciente?", "Custo por lead divide o investimento pela quantidade de contatos. Custo por paciente divide pelo número de pacientes que avançaram até o resultado definido. O segundo mostra se a campanha trouxe oportunidade de verdade."),
            ("Posso medir leads que chegam pelo WhatsApp?", "Sim, desde que o link ou a página de origem carregue um identificador antes da conversa começar. Quando a mensagem chega sem qualquer marcação, o contato pode ser registrado, mas a campanha específica não deve ser inventada."),
            ("Qual indicador usar para decidir onde investir?", "Use custo por resultado qualificado e taxa de avanço no funil, não apenas volume de leads. Uma campanha com menos contatos pode ser melhor se trouxer mais agendamentos e pacientes dentro do perfil da clínica."),
        ],
    },
    {
        "slug": "ia-no-atendimento-de-clinicas-limites",
        "title": "IA no Atendimento de Clínicas: O Que Automatizar e o Que Deve Continuar Humano",
        "seoTitle": "IA no Atendimento de Clínicas: Usos e Limites",
        "desc": "Veja onde a inteligência artificial ajuda no atendimento de clínicas, quais tarefas podem ser automatizadas e quais decisões devem continuar com a equipe de saúde.",
        "category": "Automação e IA",
        "readTime": 7,
        "heroPills": ["IA para clínicas", "Atendimento no WhatsApp", "Limites da automação"],
        "toc": [{"id":"resposta-curta","label":"Resposta curta"},{"id":"o-que-automatizar","label":"O que automatizar"},{"id":"o-que-deve-ser-humano","label":"O que deve ser humano"},{"id":"regras-de-seguranca","label":"Regras de segurança"},{"id":"como-implantar","label":"Como implantar"},{"id":"conclusao","label":"Conclusão"}],
        "faq": [
            ("O que a IA pode fazer no atendimento de uma clínica?", "Ela pode responder dúvidas frequentes, organizar informações, identificar intenção, sugerir o próximo passo, apoiar follow-up e encaminhar a conversa para a equipe. A clínica precisa definir contexto, tom, limites e momentos de transferência."),
            ("A IA pode fazer diagnóstico pelo WhatsApp?", "Não deve. Diagnóstico, conduta e indicação clínica exigem avaliação profissional. A IA pode acolher, explicar o fluxo do atendimento e encaminhar o paciente, sem transformar uma conversa comercial em decisão de saúde."),
            ("Como evitar que a IA responda algo errado?", "Use uma base de informações revisada, bloqueie assuntos fora do escopo, registre as conversas e crie uma regra clara para chamar uma pessoa. Também é importante revisar amostras reais e corrigir a configuração continuamente."),
            ("A IA substitui a recepção?", "Não. Ela reduz tarefas repetitivas e ajuda a equipe a priorizar, mas não substitui acolhimento, negociação, exceções e decisões que dependem de contexto humano. O melhor desenho divide a rotina entre automação e equipe."),
        ],
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
