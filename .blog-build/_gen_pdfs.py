#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, ListFlowable,
                                ListItem, HRFlowable, Table, TableStyle, PageBreak)

OUT = os.path.dirname(os.path.abspath(__file__))
AZUL = HexColor("#0055FE"); ESCURO = HexColor("#0D1117"); CINZA = HexColor("#5A6472")
CLARO = HexColor("#EEF3FF")

ss = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=20, textColor=AZUL, spaceAfter=6, spaceBefore=10, leading=24)
H2 = ParagraphStyle("H2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=13, textColor=ESCURO, spaceAfter=4, spaceBefore=12, leading=16)
BODY = ParagraphStyle("Body", parent=ss["Normal"], fontName="Helvetica", fontSize=10.5, textColor=ESCURO, leading=15, spaceAfter=6, alignment=TA_LEFT)
LI = ParagraphStyle("LI", parent=BODY, leftIndent=2, spaceAfter=3)
SMALL = ParagraphStyle("Small", parent=BODY, fontSize=8.5, textColor=CINZA)
COVER_SUB = ParagraphStyle("CoverSub", parent=BODY, fontSize=12, textColor=CINZA, leading=18)
QUOTE = ParagraphStyle("Quote", parent=BODY, fontName="Helvetica-Oblique", textColor=AZUL, leftIndent=10, borderPadding=4)

def bullets(items, style=LI):
    return ListFlowable([ListItem(Paragraph(t, style), leftIndent=12, value="•") for t in items],
                        bulletType="bullet", start="•", leftIndent=10)

def cover(title, subtitle):
    el = []
    el.append(Spacer(1, 3*cm))
    el.append(Paragraph("SaudeCRM", ParagraphStyle("logo", parent=BODY, fontSize=13, textColor=AZUL, fontName="Helvetica-Bold")))
    el.append(Spacer(1, 0.3*cm))
    el.append(HRFlowable(width="100%", thickness=2, color=AZUL))
    el.append(Spacer(1, 1*cm))
    el.append(Paragraph(title, ParagraphStyle("ct", parent=H1, fontSize=30, leading=36)))
    el.append(Spacer(1, 0.5*cm))
    el.append(Paragraph(subtitle, COVER_SUB))
    el.append(Spacer(1, 0.8*cm))
    el.append(Paragraph("Material gratuito para clínicas · lp.saudecrm.com", SMALL))
    el.append(PageBreak())
    return el

def cta_box():
    t = Table([[Paragraph("<b>Quer parar de fazer isso na mão?</b><br/>O SaudeCRM organiza leads, WhatsApp, follow-up e relatórios em um só lugar — com 7 dias grátis. Teste em lp.saudecrm.com.", ParagraphStyle("cta", parent=BODY, textColor=ESCURO))]],
              colWidths=[16*cm])
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),CLARO),("BOX",(0,0),(-1,-1),0.5,AZUL),
                           ("LEFTPADDING",(0,0),(-1,-1),12),("RIGHTPADDING",(0,0),(-1,-1),12),
                           ("TOPPADDING",(0,0),(-1,-1),10),("BOTTOMPADDING",(0,0),(-1,-1),10)]))
    return t

def build(path, flow):
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=2.5*cm, rightMargin=2.5*cm, topMargin=2*cm, bottomMargin=2*cm,
                            title=os.path.basename(path))
    doc.build(flow)
    print("OK", os.path.basename(path))

# ───────────────────────────────────────────────────────────────────
# PDF 1 — SPIN Selling + Treinamento da Recepção
# ───────────────────────────────────────────────────────────────────
def pdf_spin():
    e = cover("Treinamento da Recepção", "Como atender, qualificar e converter pacientes usando SPIN Selling — sem parecer vendedor")
    e += [
        Paragraph("Por que a recepção é o seu time de vendas", H1),
        Paragraph("Na maioria das clínicas, quem decide se um lead vira paciente não é o dentista nem o marketing: é a recepção. É ela que responde o WhatsApp, tira a dúvida do preço, agenda (ou não) a consulta e faz (ou esquece) o follow-up. Treinar a recepção para atender com método é o investimento de maior retorno e menor custo que uma clínica pode fazer.", BODY),
        Paragraph("Este guia ensina a recepção a usar o SPIN Selling — uma técnica consultiva criada por Neil Rackham — adaptado para a realidade de uma clínica de saúde.", BODY),

        Paragraph("O que é SPIN Selling", H2),
        Paragraph("SPIN é uma sequência de perguntas que conduz a conversa de forma natural até o paciente perceber, sozinho, que precisa do tratamento. São quatro tipos de pergunta:", BODY),
        bullets([
            "<b>S — Situação:</b> entender o contexto do paciente.",
            "<b>P — Problema:</b> descobrir a dor ou incômodo.",
            "<b>I — Implicação:</b> ampliar a consequência de não resolver.",
            "<b>N — Necessidade de solução:</b> levar o paciente a verbalizar o ganho de resolver.",
        ]),

        Paragraph("As perguntas na prática de uma clínica", H2),
        Paragraph("<b>Situação</b> — abrem a conversa sem pressão:", BODY),
        bullets(["“Há quanto tempo você está com esse incômodo?”","“Você já fez algum tratamento parecido antes?”","“O que te fez procurar a clínica agora?”"]),
        Paragraph("<b>Problema</b> — revelam a dor:", BODY),
        bullets(["“Isso tem te atrapalhado no dia a dia, pra comer ou sorrir?”","“Você sente desconforto ou é mais a estética que te incomoda?”"]),
        Paragraph("<b>Implicação</b> — mostram o custo de não agir (com cuidado e ética):", BODY),
        bullets(["“E se continuar como está, você imagina que pode piorar?”","“Já deixou de sorrir em foto ou reunião por causa disso?”"]),
        Paragraph("<b>Necessidade de solução</b> — o paciente verbaliza o ganho:", BODY),
        bullets(["“Se a gente resolvesse isso, o que mudaria pra você?”","“Voltar a sorrir tranquilo faria diferença pra você?”"]),
        cta_box(),
        PageBreak(),

        Paragraph("Roteiro de atendimento no WhatsApp (passo a passo)", H1),
        Paragraph("1. Responda rápido. O primeiro a responder geralmente fecha. Tente responder em minutos, não horas.", BODY),
        Paragraph("2. Acolha antes de vender. Cumprimente pelo nome e demonstre interesse genuíno.", BODY),
        Paragraph("3. Faça as perguntas SPIN. Não jogue o preço de cara — entenda primeiro.", BODY),
        Paragraph("4. Apresente o próximo passo, não o preço final. O objetivo da conversa é agendar a avaliação, não vender o tratamento por mensagem.", BODY),
        Paragraph("5. Conduza para o agendamento com escolha guiada: “Prefere terça de manhã ou quinta à tarde?”", BODY),
        Paragraph("6. Confirme e faça follow-up. Quem não respondeu hoje pode fechar amanhã com um lembrete gentil.", BODY),

        Paragraph("Frases que ajudam (e frases que afastam)", H2),
        Paragraph("<b>Use:</b>", BODY),
        bullets(["“Ótima pergunta! Pra te passar o valor certo, posso te fazer duas perguntinhas?”","“A avaliação é o momento de o dentista ver seu caso e te explicar tudo. Prefere de manhã ou à tarde?”"]),
        Paragraph("<b>Evite:</b>", BODY),
        bullets(["Responder só “R$ X” e parar — preço sem contexto espanta.","Deixar a pessoa no vácuo — sem follow-up, o lead vai para a concorrência.","Prometer resultado ou cura — além de antiético, fere as normas do conselho."]),

        Paragraph("Erros que fazem o paciente sumir", H2),
        bullets(["Demora pra responder.","Mandar a tabela de preços inteira sem entender o caso.","Não registrar a conversa (e esquecer de fazer follow-up).","Tom robótico ou frio.","Não ter um próximo passo claro."]),

        Paragraph("Checklist do atendimento perfeito", H2),
        bullets(["[ ] Respondi em poucos minutos","[ ] Chamei a pessoa pelo nome","[ ] Fiz ao menos 2 perguntas antes de falar de preço","[ ] Conduzi para o agendamento da avaliação","[ ] Registrei o lead e a próxima ação","[ ] Agendei o follow-up se não fechou"]),
        Spacer(1, 0.4*cm),
        cta_box(),
        Spacer(1, 0.4*cm),
        Paragraph("SaudeCRM — CRM com WhatsApp e IA para clínicas. lp.saudecrm.com", SMALL),
    ]
    build(os.path.join(OUT, "treinamento-recepcao-spin-selling-saudecrm.pdf"), e)

# ───────────────────────────────────────────────────────────────────
# PDF 2 — Checklist: O que cobrar do marketing
# ───────────────────────────────────────────────────────────────────
def pdf_marketing():
    e = cover("O Que Cobrar do Seu Marketing", "O checklist do dono de clínica para cobrar resultado da agência ou do gestor de tráfego — com clareza e sem achismo")
    e += [
        Paragraph("Pare de cobrar “mais leads”. Comece a cobrar resultado.", H1),
        Paragraph("Muitos donos de clínica investem em marketing e tráfego pago, mas não sabem o que cobrar de quem cuida disso. O resultado é a velha briga: a agência diz que os leads são bons, a recepção diz que não chega ninguém qualificado, e o dono não sabe quem está certo. Este checklist te dá os pontos exatos para cobrar — em cada etapa.", BODY),

        Paragraph("1. O que cobrar sobre os números (relatórios)", H2),
        bullets([
            "Quantos leads foram gerados no período?",
            "Qual o custo por lead (investimento ÷ leads)?",
            "De quais canais vieram (Instagram, Google, Facebook)?",
            "Qual o custo por <b>paciente fechado</b> — não só por lead?",
            "O relatório mostra a jornada até a venda, ou só impressões e cliques?",
        ]),
        Paragraph("<b>Sinal de alerta:</b> agência que só mostra “alcance”, “impressões” e “engajamento” está te entregando vaidade, não resultado.", QUOTE),

        Paragraph("2. O que cobrar sobre a qualidade dos leads", H2),
        bullets([
            "Os leads são da sua cidade / região de atendimento?",
            "Estão interessados nos procedimentos que você quer vender (e não só nos baratos)?",
            "Existe um filtro/qualificação antes de chegar na recepção?",
            "A campanha está atraindo o paciente certo, ou qualquer um?",
        ]),

        Paragraph("3. O que cobrar sobre o acompanhamento", H2),
        bullets([
            "Existe reunião periódica de resultados (semanal ou quinzenal)?",
            "A agência olha a taxa de conversão, ou só a geração de leads?",
            "Quando o resultado cai, eles avisam você — ou você que descobre?",
            "Há um plano de ação claro para o próximo mês?",
        ]),
        cta_box(),
        PageBreak(),

        Paragraph("4. A conta que separa o marketing do atendimento", H1),
        Paragraph("Antes de culpar (ou elogiar) o marketing, você precisa saber onde o paciente é perdido. Use esta lógica simples:", BODY),
        bullets([
            "<b>Leads chegam, mas ninguém agenda?</b> O problema provavelmente é o atendimento/recepção, não o marketing.",
            "<b>Leads não chegam?</b> Aí sim é o marketing/tráfego.",
            "<b>Leads chegam, agendam, mas não comparecem?</b> O problema é confirmação e relacionamento (no-show).",
            "<b>Comparecem, mas não fecham?</b> O problema é a apresentação do tratamento/preço na clínica.",
        ]),
        Paragraph("Sem medir cada etapa, você briga com a pessoa errada. Por isso a clínica precisa de um CRM: ele mostra exatamente onde o paciente some.", BODY),

        Paragraph("5. As perguntas que todo dono deveria fazer todo mês", H2),
        bullets([
            "Quantos leads entraram e quanto custaram?",
            "Quantos viraram consulta? Quantos viraram tratamento?",
            "Qual foi o faturamento gerado pelo marketing x quanto foi investido (ROI)?",
            "Qual canal trouxe o paciente mais lucrativo?",
            "O que vamos mudar no próximo mês — e por quê?",
        ]),

        Paragraph("6. Combinado saudável com a agência", H2),
        bullets([
            "Metas claras e por escrito (leads, custo por lead, e idealmente pacientes).",
            "Acesso às contas de anúncio (a conta é SUA, não da agência).",
            "Relatório simples e honesto, com os números que importam.",
            "Divisão de responsabilidade: marketing traz o lead, a clínica converte — e os dois medem.",
        ]),
        Paragraph("<b>Regra de ouro:</b> marketing bom traz lead qualificado; clínica boa converte. Sem medir as duas pontas, ninguém sabe quem precisa melhorar.", QUOTE),
        Spacer(1, 0.4*cm),
        cta_box(),
        Spacer(1, 0.4*cm),
        Paragraph("SaudeCRM — meça leads, conversão e ROI do seu marketing em um só lugar. lp.saudecrm.com", SMALL),
    ]
    build(os.path.join(OUT, "checklist-o-que-cobrar-do-marketing-saudecrm.pdf"), e)

pdf_spin()
pdf_marketing()
print("PDFs gerados")
