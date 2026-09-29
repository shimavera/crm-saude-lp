#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bloco "Leia também" curado ao fim de cada post.

Por que existe: em 15/08/2026 o blog tinha 27 posts e 13 deles não recebiam
NENHUM link interno. Os 10 artigos que vieram dos PRs #9 e #10 não linkavam
para lugar nenhum e ninguém linkava para eles — eram ilhas. Isso desperdiça
autoridade e faz o Google (e os modelos de IA) entenderem cada página como um
texto solto em vez de um conjunto sobre o mesmo assunto.

Os relacionados são CURADOS por tema, não rotativos: link aleatório entre
artigos sem relação não ajuda o leitor nem o buscador.

Idempotente. Roda depois do _build.py e do _patch_manuais.py.
"""
import os, re, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "blog")
MARK = "<!-- leia-tambem -->"

TITULOS = {
    "automacao-de-whatsapp-para-clinicas": "Automação de WhatsApp para clínicas",
    "captacao-pacientes-harmonizacao-facial": "Captação de pacientes para harmonização facial",
    "comissao-de-dentistas-como-calcular": "Comissão de dentistas: como calcular",
    "como-atrair-pacientes-clinica-odontologica": "Como atrair pacientes para clínica odontológica",
    "como-nao-perder-leads-no-whatsapp": "Como não perder leads no WhatsApp",
    "como-reduzir-faltas-no-show-consultas": "Como reduzir faltas (no-show) em consultas",
    "crm-para-clinica-de-estetica": "CRM para clínica de estética",
    "crm-para-clinica-odontologica": "CRM para clínica odontológica: guia completo",
    "crm-para-dentistas": "CRM para dentistas",
    "crm-ou-planilha-para-clinica": "CRM ou planilha para clínica",
    "equipe-minima-para-clinica": "Equipe mínima para clínica",
    "equipe-nao-consegue-acompanhar-leads": "Equipe não consegue acompanhar os leads?",
    "follow-up-de-pacientes": "Follow-up de pacientes",
    "funil-de-vendas-para-clinicas": "Funil de vendas para clínicas",
    "gestao-de-clinicas-guia": "Gestão de clínicas: as 6 frentes",
    "indicadores-clinica-odontologica": "Indicadores de uma clínica odontológica",
    "ia-no-atendimento-de-clinicas-limites": "IA no atendimento de clínicas: usos e limites",
    "lgpd-para-clinicas": "LGPD na clínica",
    "melhores-sistemas-para-clinicas": "Melhores sistemas para clínicas",
    "precificacao-consulta-clinica-medica": "Precificação de consulta em clínica médica",
    "precificacao-odontologica-hora-clinica": "Precificação odontológica e hora clínica",
    "precificacao-procedimentos-esteticos": "Precificação de procedimentos estéticos",
    "publicidade-odontologica-o-que-pode": "Publicidade odontológica: o que pode",
    "quanto-custa-crm-para-clinica": "Quanto custa um CRM para clínica",
    "recorrencia-em-clinica-de-estetica": "Recorrência em clínica de estética",
    "secretaria-ou-crm-atendimento-clinica": "Secretária ou CRM?",
    "secretaria-virtual-com-ia-para-clinicas": "Secretária virtual com IA para clínicas",
    "software-de-gestao-ou-crm-para-clinica": "Software de gestão ou CRM",
    "trafego-pago-para-dentistas": "Tráfego pago para dentistas",
    "como-saber-qual-anuncio-trouxe-paciente": "Como saber qual anúncio trouxe cada paciente",
}

# 3 relacionados por post, escolhidos por proximidade de tema e por intenção
# de leitura seguinte (quem leu X provavelmente decide Y depois).
RELACIONADOS = {
    "crm-para-dentistas": ["quanto-custa-crm-para-clinica", "software-de-gestao-ou-crm-para-clinica", "melhores-sistemas-para-clinicas"],
    "crm-para-clinica-odontologica": ["crm-para-dentistas", "quanto-custa-crm-para-clinica", "melhores-sistemas-para-clinicas"],
    "crm-ou-planilha-para-clinica": ["software-de-gestao-ou-crm-para-clinica", "crm-para-dentistas", "melhores-sistemas-para-clinicas"],
    "crm-para-clinica-de-estetica": ["recorrencia-em-clinica-de-estetica", "precificacao-procedimentos-esteticos", "captacao-pacientes-harmonizacao-facial"],
    "melhores-sistemas-para-clinicas": ["quanto-custa-crm-para-clinica", "software-de-gestao-ou-crm-para-clinica", "crm-para-dentistas"],
    "quanto-custa-crm-para-clinica": ["melhores-sistemas-para-clinicas", "crm-para-dentistas", "indicadores-clinica-odontologica"],
    "software-de-gestao-ou-crm-para-clinica": ["crm-para-dentistas", "melhores-sistemas-para-clinicas", "quanto-custa-crm-para-clinica"],

    "como-nao-perder-leads-no-whatsapp": ["follow-up-de-pacientes", "automacao-de-whatsapp-para-clinicas", "funil-de-vendas-para-clinicas"],
    "automacao-de-whatsapp-para-clinicas": ["secretaria-virtual-com-ia-para-clinicas", "como-nao-perder-leads-no-whatsapp", "como-reduzir-faltas-no-show-consultas"],
    "ia-no-atendimento-de-clinicas-limites": ["automacao-de-whatsapp-para-clinicas", "secretaria-virtual-com-ia-para-clinicas", "lgpd-para-clinicas"],
    "follow-up-de-pacientes": ["funil-de-vendas-para-clinicas", "equipe-nao-consegue-acompanhar-leads", "como-nao-perder-leads-no-whatsapp"],
    "funil-de-vendas-para-clinicas": ["indicadores-clinica-odontologica", "follow-up-de-pacientes", "crm-para-dentistas"],
    "equipe-nao-consegue-acompanhar-leads": ["secretaria-ou-crm-atendimento-clinica", "follow-up-de-pacientes", "equipe-minima-para-clinica"],
    "secretaria-ou-crm-atendimento-clinica": ["secretaria-virtual-com-ia-para-clinicas", "equipe-minima-para-clinica", "automacao-de-whatsapp-para-clinicas"],
    "secretaria-virtual-com-ia-para-clinicas": ["secretaria-ou-crm-atendimento-clinica", "automacao-de-whatsapp-para-clinicas", "equipe-minima-para-clinica"],

    "como-atrair-pacientes-clinica-odontologica": ["trafego-pago-para-dentistas", "publicidade-odontologica-o-que-pode", "crm-para-dentistas"],
    "trafego-pago-para-dentistas": ["publicidade-odontologica-o-que-pode", "como-atrair-pacientes-clinica-odontologica", "indicadores-clinica-odontologica"],
    "como-saber-qual-anuncio-trouxe-paciente": ["trafego-pago-para-dentistas", "indicadores-clinica-odontologica", "funil-de-vendas-para-clinicas"],
    "captacao-pacientes-harmonizacao-facial": ["precificacao-procedimentos-esteticos", "recorrencia-em-clinica-de-estetica", "crm-para-clinica-de-estetica"],
    "publicidade-odontologica-o-que-pode": ["trafego-pago-para-dentistas", "como-atrair-pacientes-clinica-odontologica", "lgpd-para-clinicas"],

    "gestao-de-clinicas-guia": ["indicadores-clinica-odontologica", "equipe-minima-para-clinica", "como-reduzir-faltas-no-show-consultas"],
    "indicadores-clinica-odontologica": ["gestao-de-clinicas-guia", "funil-de-vendas-para-clinicas", "precificacao-odontologica-hora-clinica"],
    "equipe-minima-para-clinica": ["secretaria-ou-crm-atendimento-clinica", "comissao-de-dentistas-como-calcular", "gestao-de-clinicas-guia"],
    "como-reduzir-faltas-no-show-consultas": ["automacao-de-whatsapp-para-clinicas", "gestao-de-clinicas-guia", "indicadores-clinica-odontologica"],
    "comissao-de-dentistas-como-calcular": ["precificacao-odontologica-hora-clinica", "equipe-minima-para-clinica", "gestao-de-clinicas-guia"],

    "precificacao-odontologica-hora-clinica": ["precificacao-consulta-clinica-medica", "comissao-de-dentistas-como-calcular", "indicadores-clinica-odontologica"],
    "precificacao-consulta-clinica-medica": ["precificacao-odontologica-hora-clinica", "gestao-de-clinicas-guia", "como-reduzir-faltas-no-show-consultas"],
    "precificacao-procedimentos-esteticos": ["recorrencia-em-clinica-de-estetica", "precificacao-odontologica-hora-clinica", "crm-para-clinica-de-estetica"],
    "recorrencia-em-clinica-de-estetica": ["crm-para-clinica-de-estetica", "precificacao-procedimentos-esteticos", "captacao-pacientes-harmonizacao-facial"],

    "lgpd-para-clinicas": ["publicidade-odontologica-o-que-pode", "secretaria-virtual-com-ia-para-clinicas", "gestao-de-clinicas-guia"],
}


def bloco(slug, indent):
    itens = "".join(
        f'{indent}  <li><a href="/blog/{r}.html">{TITULOS[r]}</a></li>\n'
        for r in RELACIONADOS[slug])
    return (f'\n{MARK}\n'
            f'{indent}<h2 id="leia-tambem">Leia também</h2>\n'
            f'{indent}<ul>\n{itens}{indent}</ul>\n')


def main():
    faltando = [s for s in TITULOS if s not in RELACIONADOS]
    if faltando:
        sys.exit(f"Sem relacionados definidos: {faltando}")

    for slug, rels in RELACIONADOS.items():
        path = os.path.join(OUT, f"{slug}.html")
        if not os.path.exists(path):
            print(f"-- {slug}: não existe, pulado"); continue
        t = open(path, encoding="utf-8").read()
        if MARK in t:
            print(f"== {slug}: já tem"); continue

        # entra antes das Fontes quando existirem, senão no fim do artigo
        alvo = '<!-- fontes-externas -->'
        indent = "        "
        if alvo in t:
            i = t.index(alvo)
            t = t[:i] + bloco(slug, indent).lstrip("\n") + t[i:]
        else:
            fecha = "        </article>" if "        </article>" in t else "</article>"
            t = t.replace(fecha, bloco(slug, indent) + fecha, 1)

        # reflete na lista lateral de navegação, quando houver
        if 'href="#leia-tambem"' not in t:
            m = re.search(r'(<ul class="toc-list">.*?)(\n\s*</ul>)', t, re.S)
            if m and 'href="#fontes"' in t:
                t = t.replace('<li><a href="#fontes">Fontes</a></li>',
                              '<li><a href="#leia-tambem">Leia também</a></li>\n            <li><a href="#fontes">Fontes</a></li>', 1)
        open(path, "w", encoding="utf-8").write(t)
        print(f"OK {slug}: +3 links ({', '.join(rels)})")


if __name__ == "__main__":
    main()
