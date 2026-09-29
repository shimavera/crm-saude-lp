/* Interface reconstruída para demonstração visual. Todos os dados são fictícios. */
const paths = {
  grid: '<rect x="3" y="3" width="6" height="6" rx="1"/><rect x="15" y="3" width="6" height="6" rx="1"/><rect x="3" y="15" width="6" height="6" rx="1"/><rect x="15" y="15" width="6" height="6" rx="1"/>',
  chat: '<path d="M21 14a3 3 0 0 1-3 3H8l-5 4V6a3 3 0 0 1 3-3h12a3 3 0 0 1 3 3z"/>',
  kanban: '<path d="M4 4v16M12 4v11M20 4v16"/>',
  people: '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2M22 21v-2a4 4 0 0 0-3-3.87M16 3a4 4 0 0 1 0 8"/><circle cx="9" cy="7" r="4"/>',
  calendar: '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M16 3v4M8 3v4M3 11h18"/>',
  check: '<path d="M20 11v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h10M9 11l3 3L22 3"/>',
  flow: '<circle cx="6" cy="5" r="3"/><circle cx="18" cy="7" r="3"/><circle cx="6" cy="19" r="3"/><path d="M6 8v8M9 17l7-7"/>',
  speaker: '<path d="M3 10h4l12-5v14L7 14H3zM7 14l2 7h4l-2-6M22 9v6"/>',
  target: '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
  search: '<circle cx="10" cy="10" r="6"/><path d="m15 15 6 6"/>',
  clock: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
  mic: '<rect x="8" y="2" width="8" height="13" rx="4"/><path d="M5 10v2a7 7 0 0 0 14 0v-2M12 19v3M8 22h8"/>',
  arrow: '<path d="m3 17 6-6 4 4 8-11M15 4h6v6"/>',
  money: '<path d="M12 2v20M17 5H9a4 4 0 0 0 0 8h6a4 4 0 0 1 0 8H5"/>',
  heart: '<path d="M12 21S2 15 2 8a5 5 0 0 1 10-1 5 5 0 0 1 10 1c0 7-10 13-10 13zM5 11h4l2-4 3 9 2-5h3"/>',
};
const icon = (name, size = 20) => `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${paths[name] || paths.chat}</svg>`;
const view = new URLSearchParams(location.search).get('view') || 'dashboard';
const activeView = ['dashboard', 'conversas', 'kanban'].includes(view) ? view : 'dashboard';
const nav = [['grid','Visão Geral','dashboard'],['chat','Conversas Ativas','conversas'],['kanban','Kanban','kanban'],['people','Contatos',''],['calendar','Agenda',''],['check','Atividades',''],['flow','Fluxos',''],['speaker','Disparos',''],['target','Rastreio','']];
document.getElementById('sidebar').innerHTML = `
  <div class="brand"><span class="brand-mark">${icon('heart')}</span><span>SaúdeCRM</span><span class="collapse">◧</span></div>
  <nav class="nav" aria-label="Navegação ilustrativa">${nav.map(([symbol,label,key]) => `<div class="nav-item ${activeView === key ? 'active' : ''}"><span class="icon">${icon(symbol)}</span>${label}${key === '' && label === 'Atividades' ? '<span class="notification">3</span>' : ''}</div>`).join('')}</nav>
  <div class="side-bottom"><div class="profile"><span class="avatar">M</span><div><strong>Marina</strong><small>Clínica Demonstração</small></div><span class="collapse">⌃</span></div><div class="version">☾ <span>SAÚDE IA · VISÃO DO PRODUTO</span></div><div class="demo-label"><strong>Interface demonstrativa do SaúdeCRM</strong>Dados fictícios</div></div>`;

function dashboard() {
  const metrics = [['money','Faturamento fechado','R$ 42.600,00'],['money','Oportunidades em aberto','R$ 78.400,00'],['money','Ticket médio','R$ 5.325,00'],['check','Vendas fechadas','8']];
  const chartValues = [4500, 0, 6000, 0, 4000, 7500, 0, 5500, 12000, 3100];
  const points = chartValues.map((value,i) => [47+i*68,205-value/12000*180]);
  const chartPath = points.reduce((path,[x,y],i) => i ? path + ` C${x-34} ${points[i-1][1]} ${x-34} ${y} ${x} ${y}` : `M${x} ${y}`, '');
  return `<div class="dashboard">
    <section class="hero-panel"><div class="eyebrow"><i></i> Panorama do período</div><h1>Mais clareza para<br><em>cada decisão.</em></h1><p>Acompanhe o que está em movimento e encontre as<br>próximas oportunidades da clínica.</p><div class="hero-mini"><span>Oportunidades em aberto</span><strong>24</strong></div></section>
    <div class="metrics">${metrics.map(([symbol,label,value]) => `<div class="metric"><div class="metric-icon">${icon(symbol)}</div><div class="metric-label">${label}</div><strong>${value}</strong></div>`).join('')}</div>
    <section class="chart-panel"><div class="panel-head"><div><span class="overline">RESULTADO</span><h2>Evolução do faturamento</h2><p>Vendas fechadas pela data de fechamento, no período demonstrativo.</p></div><div class="panel-total">R$ 42.600,00<small>valores inteiramente fictícios</small></div></div><div class="chart-content"><div class="graph">
      <svg viewBox="0 0 680 255" role="img" aria-label="Gráfico ilustrativo com valores financeiros fictícios"><defs><linearGradient id="fill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7286ef" stop-opacity=".15"/><stop offset="1" stop-color="#7286ef" stop-opacity="0"/></linearGradient></defs>
      ${[25,70,115,160,205].map((y,i) => `<line x1="56" y1="${y}" x2="674" y2="${y}" stroke="#e6ecf7"/><text x="45" y="${y+4}" fill="#a5afc2" font-family="Jakarta" font-size="10" text-anchor="end">${i===4?'R$ 0':'R$ '+(12-i*3)+' mil'}</text>`).join('')}
      <path d="${chartPath} L659 205 L47 205 Z" fill="url(#fill)"/>
      <path d="${chartPath}" fill="none" stroke="#6274e9" stroke-width="3"/>
      ${['02/09','05/09','08/09','11/09','14/09','17/09','20/09','23/09','26/09','29/09'].map((d,i) => `<text x="${47+i*68}" y="230" fill="#a5afc2" font-family="Jakarta" font-size="10" text-anchor="middle">${d}</text>`).join('')}</svg>
    </div><div class="summary"><h3>RESUMO DO PERÍODO</h3><div class="summary-row">Vendas fechadas<strong>8</strong></div><div class="summary-row">Ticket médio<strong>R$ 5.325,00</strong></div><p>Valores fictícios de demonstração. O ticket considera vendas com valor preenchido.</p></div></div></section>
    <div class="dashboard-footer"><div class="mini-card">PRÓXIMA AÇÃO<strong>6 conversas aguardam a equipe</strong></div><div class="mini-card">AGENDA DE EXEMPLO<strong>Próximos horários organizados por profissional</strong></div></div>
  </div>`;
}

function conversations() {
  const people = [['Helena R.','Posso no período da tarde.','Agendando','#f5d5e7'],['Felipe C.','Áudio recebido','Novo contato','#d3f2e9'],['Clara M.','Perfeito, obrigada!','Agendado','#d4dffc'],['Bianca L.','Quero saber os horários.','Em conversa','#efdcfb'],['André T.','Pode me mandar o endereço?','Agendado','#d6e6fa'],['Laura P.','Retorno combinado','Follow-up','#fff0c8'],['Otávio S.','Imagem recebida','Em conversa','#d8edf0'],['Nina F.','Obrigada pela atenção.','Concluído','#e6dfff']];
  const wave = [7,12,20,14,9,23,15,10,18,27,17,13,22,29,19,12,25,18,10,16,24,14,21,27,18,12,22,16,24,11,20,28,16,10];
  return `<div class="demo-topline"><strong>✧ IA de atendimento · visualização demonstrativa</strong><span>Exemplo de conversa com dados fictícios</span></div><div class="conversation-layout">
    <aside class="conversation-list"><div class="list-tools"><div class="list-title">CONVERSAS<div class="list-actions"><span class="select-btn">☑ Selecionar</span>${icon('search',14)}</div></div><div class="search">${icon('search')} Buscar por nome ou número...</div><div class="filter-tabs"><span>Todos <b class="count-pill">84</b></span><span>Sem resposta <b class="count-pill">6</b></span></div></div>
    ${people.map(([name,preview,stage,color],i) => `<div class="person ${i===2?'selected':''}"><div class="person-avatar" style="background:${color}">${name[0]}</div><div class="person-content"><div class="person-row"><strong>${name}</strong><time>${i!==2?'<i class="status-dot"></i>':''}Hoje ${10-i%3}:${i%2?'24':'18'}</time></div><div class="person-preview"><span><b>${i===0?'':'Você: '}</b>${preview}</span><small>${stage}</small></div></div></div>`).join('')}</aside>
    <section class="chat-column"><header class="chat-header"><div class="person-avatar" style="background:#e7e0fc">C</div><div class="chat-name"><strong>Clara M.</strong><span>Contato demonstrativo</span></div><span class="campaign-pill">${icon('speaker',16)}<span>QUERO CONHECER A CLÍNICA<br>Campanha ilustrativa · avaliação inicial</span></span><span class="channel-pill">Instagram</span><div class="chat-header-actions"><span class="square-tool">⋮</span><span class="stage-pill">↗ Agendado</span>${icon('search',19)}</div></header>
    <div class="chat-history"><div class="day-divider"><span>HOJE · CONVERSA ILUSTRATIVA</span></div>
      <div class="bubble in">Olá! Gostaria de conhecer a clínica.<span class="time">09:12</span></div>
      <div class="bubble out">Oi, Clara! Que bom receber sua mensagem.<br>Você procura um horário pela manhã ou à tarde?<span class="time">09:12 <b class="check">✓✓</b></span></div>
      <div class="bubble in"><div class="audio-illustration"><span class="audio-icon">${icon('mic',20)}</span><div class="audio-wave">${wave.map(h=>`<i style="height:${h}px"></i>`).join('')}</div></div><div class="audio-details"><span>Áudio ilustrativo · 0:12</span><span>09:13</span></div><div class="transcription">Exemplo visual, sem gravação de paciente.</div></div>
      <div class="bubble out">Entendi! O período da tarde fica melhor para você.<br>Posso verificar um horário com a Dra. Elisa?<span class="time">09:13 <b class="check">✓✓</b></span></div>
      <div class="bubble in">Pode sim. Na quinta-feira seria ótimo!<span class="time">09:14</span></div>
      <div class="system-note">✧ Preferência registrada · equipe acompanha o histórico</div>
      <div class="bubble out">Combinado, Clara. Veja este exemplo de agendamento:<div class="appointment">${icon('calendar',24)}<div><strong>Quinta-feira · 15h30</strong><span>Avaliação inicial · Dra. Elisa (fictícia)</span></div></div>Se precisar de ajuda, nossa equipe está por aqui.<span class="time">09:15 <b class="check">✓✓</b></span></div>
      <div class="bubble in">Perfeito, obrigada!<span class="time">09:16</span></div>
    </div><div class="chat-compose no-controls"><span style="font-size:27px">+</span><div class="compose-input">Envie uma mensagem (Intervenção)... <span style="font-size:22px">☺</span></div><span class="mic-icon">${icon('mic')}</span></div></section></div>`;
}

function kanban() {
  const stats = [['ENTRADAS NO PERÍODO','56','contatos neste exemplo','#8170f3','#eeebfc'],['CLOSE RATE','14,3%','8 de 56 contatados','#2cb794','#edf8f3'],['TAXA DE PERDA','10,7%','6 de 56 contatados','#ee6d7a','#fff0f0'],['EM ANDAMENTO','24','contatos no exemplo','#7569ed','#f0edff'],['1ª RESPOSTA','38s','mediana ilustrativa','#eea23c','#fff7e9'],['AGUARDANDO','6','sem resposta','#ee6d7a','#fff0f0'],['FECHAMENTOS','R$ 42.600','8 fechados no período','#21aa8a','#edf8f4'],['OPORTUNIDADES','R$ 78.400','valores fictícios','#2cabe0','#eaf6ff']];
  const columns = [
    ['Novo contato','people','8','#8171fd','#eae6ff',['Luísa B.','Caio D.','Sofia A.','Vitor N.']],
    ['Contato iniciado','chat','6','#2babdf','#e0f3fc',['Bruno V.','Cecília O.','Alice D.','Theo C.']],
    ['Em follow-up','clock','5','#f19431','#fff0db',['Beatriz E.','Ícaro P.','Lívia H.','Hugo L.']],
    ['Consulta agendada','calendar','4','#efa325','#fff2d9',['Clara M.','Lara W.','Pedro X.','Isabel G.']],
    ['Qualificando','arrow','1','#9b73f6','#eee6ff',['Marina Z.','Enzo K.','Maya J.','Leandro I.']],
  ];
  return `<div class="kanban-header"><div class="kanban-heading"><h2>Pré-consulta / Venda <span style="font-size:16px;color:#8ca0bc;margin-left:9px">⚙</span></h2><p>56 contatos neste funil · dados demonstrativos</p></div><div class="kanban-toolbar"><div class="search">${icon('search',18)} Buscar por nome ou telefone...</div><span class="filter-tool">▽ Filtros <span style="font-size:9px">●</span></span><span class="metric-tool">${icon('arrow',18)} Ocultar métricas</span></div></div>
    <div class="kanban-metrics">${stats.map(([label,value,detail,accent,tint])=>`<div class="kanban-stat" style="--accent:${accent};--tint:${tint}"><small>${label} ↗</small><strong>${value}</strong><span>${detail}</span></div>`).join('')}</div><div class="kanban-scroll-track"></div>
    <div class="board">${columns.map(([title,symbol,count,accent,tint,names],ci)=>`<section class="column" style="--accent:${accent};--tint:${tint}"><div class="column-head"><span class="checkbox"></span>${icon(symbol,15)}<strong>${title}</strong><span class="count-pill">${count}</span></div>${names.map((name,i)=>`<article class="lead-card"><div class="lead-card-top"><span class="checkbox"></span><h3>${name}</h3><span class="lead-chat">▢</span><span style="color:#b0bbcb">···</span></div><p class="lead-subtitle">Contato demonstrativo</p><span class="lead-tag">${icon('speaker',11)} ${['Instagram','Google','Facebook','Indicação'][(i+ci)%4]}</span><div class="lead-owner"><span class="owner-avatar">MA</span>Marina A. · recepção</div><span class="lead-chip ${i%2?'green':''}">${ci===3?'Horário reservado':ci===2?'Retomar conversa':ci===4?'Preferência registrada':'Avaliação inicial'}</span><div class="lead-date">${icon('clock',10)} ${ci===3?'Quinta · 15h30':'1º contato '+['Hoje','Ontem','Há 2 dias','Há 3 dias'][i]}</div></article>`).join('')}</section>`).join('')}</div><div class="kanban-bottom"><span>Organize cada contato e acompanhe a próxima ação.</span><span>Interface demonstrativa · todos os dados são fictícios</span></div>`;
}

const screen = document.getElementById('screen');
screen.className = activeView === 'conversas' ? 'conversation-screen' : activeView === 'kanban' ? 'kanban-screen' : '';
screen.innerHTML = activeView === 'conversas' ? conversations() : activeView === 'kanban' ? kanban() : dashboard();
document.documentElement.dataset.view = activeView;
