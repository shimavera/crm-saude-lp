#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, html
BLOG = os.path.dirname(os.path.abspath(__file__))

# slug -> (material_key, titulo do box, descrição, badge/formato)
MAP = {
  "como-nao-perder-leads-no-whatsapp": ("atendimento", "Planilha de Atendimento e Follow-up", "Controle todos os seus leads e follow-ups em uma planilha pronta (Excel). Do primeiro contato ao paciente fechado.", "Planilha · Excel"),
  "follow-up-de-pacientes": ("atendimento", "Planilha de Atendimento e Follow-up", "Organize o follow-up de cada lead em uma planilha pronta para usar hoje — com etapas, próxima ação e resumo automático.", "Planilha · Excel"),
  "indicadores-clinica-odontologica": ("metricas", "Planilha de Indicadores da Clínica", "Acompanhe captação, conversão, no-show, ticket médio e ROI em uma planilha que calcula tudo sozinha.", "Planilha · Excel"),
  "funil-de-vendas-para-clinicas": ("metricas", "Planilha de Indicadores da Clínica", "Meça a conversão de cada etapa do seu funil em uma planilha pronta — só preencher e acompanhar.", "Planilha · Excel"),
  "secretaria-ou-crm-atendimento-clinica": ("recepcao", "Guia de Treinamento da Recepção (SPIN Selling)", "Um PDF para treinar sua recepção a atender, qualificar e converter pacientes no WhatsApp — com roteiro e frases prontas.", "PDF · Treinamento"),
  "trafego-pago-para-dentistas": ("marketing", "Checklist: O Que Cobrar do Seu Marketing", "O guia do dono de clínica para cobrar resultado da agência ou do gestor de tráfego — com clareza e sem achismo.", "PDF · Checklist"),
  "como-atrair-pacientes-clinica-odontologica": ("marketing", "Checklist: O Que Cobrar do Seu Marketing", "Saiba exatamente o que exigir de quem cuida do seu marketing — relatórios, qualidade de leads e ROI.", "PDF · Checklist"),
  "automacao-de-whatsapp-para-clinicas": ("atendimento", "Planilha de Atendimento e Follow-up", "Enquanto não automatiza tudo, organize seus leads e follow-ups nesta planilha pronta (Excel).", "Planilha · Excel"),
  "como-reduzir-faltas-no-show-consultas": ("metricas", "Planilha de Indicadores da Clínica", "Acompanhe sua taxa de no-show e outros indicadores nesta planilha que calcula tudo automaticamente.", "Planilha · Excel"),
  "crm-para-clinica-de-estetica": ("metricas", "Planilha de Indicadores da Clínica", "Meça conversão, recompra e ticket médio da sua clínica de estética nesta planilha pronta.", "Planilha · Excel"),
}

def esc(s): return html.escape(s, quote=True)

def box(material, titulo, desc, badge):
    return f'''
          <!-- MATERIAL RICO (lead magnet) -->
          <div class="material-box" data-material="{material}">
            <div class="material-badge">{esc(badge)} · grátis</div>
            <h3>{esc(titulo)}</h3>
            <p>{esc(desc)}</p>
            <button type="button" class="material-trigger" onclick="abrirMaterial('{material}','{esc(titulo)}')">Baixar material grátis →</button>
          </div>
'''

STYLE_MODAL = '''
  <style>
    .material-box{background:linear-gradient(135deg,#0055FE,#1A6BFF);border-radius:18px;padding:26px 24px;margin:32px 0;color:#fff;box-shadow:0 8px 30px rgba(0,85,254,.22)}
    .material-box .material-badge{display:inline-block;background:rgba(255,255,255,.18);color:#fff;font-size:11px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;padding:5px 12px;border-radius:100px;margin-bottom:12px}
    .material-box h3{color:#fff !important;margin:0 0 8px;font-size:1.25rem;font-weight:800}
    .material-box p{color:rgba(255,255,255,.92) !important;margin:0 0 18px;font-size:.95rem;line-height:1.55}
    .material-trigger{background:#fff;color:#0055FE;border:none;border-radius:12px;padding:13px 24px;font-weight:700;font-size:.95rem;cursor:pointer;font-family:inherit;transition:transform .15s}
    .material-trigger:hover{transform:translateY(-2px)}
    .mat-overlay{position:fixed;inset:0;background:rgba(13,17,23,.6);backdrop-filter:blur(4px);display:none;align-items:center;justify-content:center;z-index:9999;padding:20px}
    .mat-overlay.open{display:flex}
    .mat-modal{background:#fff;border-radius:20px;max-width:440px;width:100%;padding:32px;box-shadow:0 20px 60px rgba(0,0,0,.3);position:relative}
    .mat-modal h3{margin:0 0 6px;font-size:1.3rem;font-weight:800;color:#0D1117}
    .mat-modal .mat-sub{color:#5A6472;font-size:.9rem;margin:0 0 20px}
    .mat-close{position:absolute;top:16px;right:18px;background:none;border:none;font-size:24px;color:#8A96A8;cursor:pointer;line-height:1}
    .mat-field{margin-bottom:14px}
    .mat-field label{display:block;font-size:.8rem;font-weight:600;color:#1A2230;margin-bottom:5px}
    .mat-field input{width:100%;padding:12px 14px;border:1px solid #D4DBE8;border-radius:10px;font-size:.95rem;font-family:inherit;outline:none;box-sizing:border-box}
    .mat-field input:focus{border-color:#0055FE}
    .mat-submit{width:100%;background:#0055FE;color:#fff;border:none;border-radius:12px;padding:14px;font-weight:700;font-size:1rem;cursor:pointer;font-family:inherit;margin-top:6px}
    .mat-submit:disabled{opacity:.6;cursor:default}
    .mat-success{text-align:center;padding:10px 0}
    .mat-success .mat-check{width:56px;height:56px;border-radius:50%;background:#EEF3FF;color:#0055FE;display:flex;align-items:center;justify-content:center;margin:0 auto 14px;font-size:28px}
    .mat-priv{font-size:.72rem;color:#8A96A8;text-align:center;margin-top:12px}
    .mat-err{color:#dc2626;font-size:.8rem;margin-top:8px;display:none}
  </style>

  <div class="mat-overlay" id="matOverlay" role="dialog" aria-modal="true">
    <div class="mat-modal">
      <button class="mat-close" onclick="fecharMaterial()" aria-label="Fechar">&times;</button>
      <div id="matFormWrap">
        <h3 id="matTitulo">Receba o material grátis</h3>
        <p class="mat-sub">Preencha para baixar agora. Sem custo, sem compromisso.</p>
        <form id="matForm">
          <div class="mat-field"><label>Nome</label><input type="text" name="nome" required placeholder="Seu nome" autocomplete="name"></div>
          <div class="mat-field"><label>E-mail</label><input type="email" name="email" required placeholder="seu@email.com" autocomplete="email"></div>
          <div class="mat-field"><label>WhatsApp (opcional)</label><input type="tel" name="whatsapp" placeholder="(11) 90000-0000" autocomplete="tel"></div>
          <button type="submit" class="mat-submit" id="matSubmit">Baixar agora →</button>
          <div class="mat-err" id="matErr">Algo deu errado. Tente novamente.</div>
        </form>
        <p class="mat-priv">Seus dados estão seguros. Usamos apenas para enviar o material e novidades do SaudeCRM.</p>
      </div>
      <div class="mat-success" id="matSuccess" style="display:none">
        <div class="mat-check">✓</div>
        <h3>Pronto! Seu material está baixando.</h3>
        <p class="mat-sub">Se o download não começar, <a href="#" id="matDirectLink" style="color:#0055FE;font-weight:600">clique aqui</a>.</p>
        <a href="https://saudecrm.com/cadastro" class="mat-submit" style="display:block;text-decoration:none;text-align:center;margin-top:10px">Conhecer o SaudeCRM grátis →</a>
      </div>
    </div>
  </div>

  <script>
    var _matCurrent = null;
    function abrirMaterial(mat, titulo){
      _matCurrent = mat;
      document.getElementById('matTitulo').textContent = titulo || 'Receba o material grátis';
      document.getElementById('matFormWrap').style.display = 'block';
      document.getElementById('matSuccess').style.display = 'none';
      document.getElementById('matErr').style.display = 'none';
      document.getElementById('matOverlay').classList.add('open');
      if (window.clarity) try { clarity('event','material_open_'+mat); } catch(e){}
    }
    function fecharMaterial(){ document.getElementById('matOverlay').classList.remove('open'); }
    document.getElementById('matOverlay').addEventListener('click', function(e){ if(e.target===this) fecharMaterial(); });
    document.getElementById('matForm').addEventListener('submit', async function(e){
      e.preventDefault();
      var btn = document.getElementById('matSubmit'); var err = document.getElementById('matErr');
      btn.disabled = true; btn.textContent = 'Enviando...'; err.style.display='none';
      var fd = new FormData(this);
      var payload = { nome: fd.get('nome'), email: fd.get('email'), whatsapp: fd.get('whatsapp'), material: _matCurrent };
      try{
        var r = await fetch('/api/material', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload) });
        var data = await r.json();
        if(!r.ok || !data.url) throw new Error('fail');
        // dispara download
        var a = document.createElement('a'); a.href = data.url; a.download = ''; document.body.appendChild(a); a.click(); a.remove();
        document.getElementById('matDirectLink').href = data.url;
        document.getElementById('matFormWrap').style.display='none';
        document.getElementById('matSuccess').style.display='block';
        if (window.dataLayer) window.dataLayer.push({event:'material_download', material:_matCurrent});
        if (window.clarity) try { clarity('event','material_download_'+_matCurrent); } catch(e){}
      }catch(_){ err.style.display='block'; }
      finally{ btn.disabled=false; btn.textContent='Baixar agora →'; }
    });
  </script>
'''

count = 0
for slug,(mat,titulo,desc,badge) in MAP.items():
    path = os.path.join(BLOG, f"{slug}.html")
    if not os.path.exists(path):
        print("SKIP (não existe):", slug); continue
    h = open(path, encoding="utf-8").read()
    if "material-box" in h:
        print("já tem material:", slug); continue
    # inserir o box antes da conclusão
    marker = '<h2 id="conclusao"'
    if marker in h:
        h = h.replace(marker, box(mat,titulo,desc,badge) + "\n          " + marker, 1)
    else:
        # fallback: antes do fim do article-content
        h = h.replace("        </article>", box(mat,titulo,desc,badge) + "        </article>", 1)
    # inserir modal+style+js antes de </body>
    h = h.replace("</body>", STYLE_MODAL + "\n</body>", 1)
    open(path,"w",encoding="utf-8").write(h)
    count += 1
    print("OK material em", slug, "->", mat)
print("Total artigos com material:", count)
