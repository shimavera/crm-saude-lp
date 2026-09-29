
(() => {
  'use strict';
  const root = document.documentElement;
  const media = window.matchMedia('(prefers-reduced-motion: reduce)');
  const motionButton = document.getElementById('motion-toggle');
  let manualPause = false;
  let paused = media.matches;
  let heroVisible = true;
  let frame = 0;
  let previousFrame = 0;
  let drawTime = 0;
  const canvas = document.getElementById('signal-canvas');
  const context = canvas ? canvas.getContext('2d') : null;
  const dashboard = document.getElementById('hero-dashboard');
  const baseTransform = 'rotateY(-18deg) rotateX(12deg) rotateZ(-7deg)';

  function updateMotion() {
    paused = manualPause || media.matches;
    root.classList.toggle('motion-paused', paused);
    motionButton.setAttribute('aria-pressed', String(paused));
    motionButton.querySelector('span').textContent = paused ? 'Ativar animações' : 'Pausar animações';
    if (dashboard) dashboard.style.transform = '';
    if (paused) {
      cancelAnimationFrame(frame);
      frame = 0;
      if (context) drawSignals(drawTime);
    } else startCanvas();
  }
  motionButton.addEventListener('click', () => {
    if (media.matches) {
      manualPause = !manualPause;
      motionButton.querySelector('span').textContent = 'Movimento reduzido ativo';
      motionButton.setAttribute('aria-pressed', 'true');
      return;
    }
    manualPause = !manualPause;
    updateMotion();
  });
  media.addEventListener('change', updateMotion);
  root.classList.add('js-ready');
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -20px 0px' });
    document.querySelectorAll('.reveal').forEach(node => observer.observe(node));
  } else document.querySelectorAll('.reveal').forEach(node => node.classList.add('is-visible'));

  const menuButton = document.querySelector('.menu-toggle');
  const menu = document.getElementById('mobile-menu');
  const setMenu = open => {
    menu.hidden = !open;
    menuButton.setAttribute('aria-expanded', String(open));
    menuButton.setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu');
  };
  menuButton.addEventListener('click', () => setMenu(menu.hidden));
  menu.querySelectorAll('a').forEach(link => link.addEventListener('click', () => setMenu(false)));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && !menu.hidden) { setMenu(false); menuButton.focus(); }
  });

  const scenes = [
    { title: 'O atendimento começa aqui', subtitle: 'IA de atendimento · SaúdeCRM', patient: 'Oi! Vocês fazem avaliação?', answer: 'Olá! Vamos te ajudar. Me conta: é sua primeira visita à clínica?', insight: 'Uma pergunta simples. Um atendimento com contexto.' },
    { title: 'Uma conversa merece continuidade', subtitle: 'Follow-up · SaúdeCRM', patient: 'Vou olhar com calma e depois retorno.', answer: 'Olá! Ficou alguma dúvida sobre a avaliação? Se quiser continuar, nossa equipe pode te ajudar com o próximo passo.', insight: 'O retorno segue o contexto e as regras da sua clínica.' },
    { title: 'Sua equipe entra com o contexto', subtitle: 'Atendimento humano · SaúdeCRM', patient: 'Quero conversar com alguém da equipe.', answer: 'Com certeza. Vou encaminhar sua conversa para a equipe. Assim, ela continua o atendimento com o que você já compartilhou.', insight: 'O histórico acompanha o atendimento. O cuidado continua.' }
  ];
  const tabs = Array.from(document.querySelectorAll('[data-scene]'));
  const scenePanel = document.getElementById('demo-panel');
  const messages = document.getElementById('scene-messages');
  let currentScene = 0;
  function selectScene(index, focus = false) {
    const scene = scenes[index];
    currentScene = index;
    tabs.forEach((tab, tabIndex) => {
      const selected = tabIndex === index;
      tab.setAttribute('aria-selected', String(selected));
      tab.tabIndex = selected ? 0 : -1;
    });
    scenePanel.setAttribute('aria-labelledby', tabs[index].id);
    document.getElementById('scene-title').textContent = scene.title;
    document.getElementById('scene-subtitle').textContent = scene.subtitle;
    messages.innerHTML = '<div class="scene-message from-patient"><span>PACIENTE</span>' + scene.patient + '</div><div class="scene-message from-ai"><span><svg><use href="#i-spark"/></svg> SAÚDECRM IA</span>' + scene.answer + '</div><div class="scene-insight"><svg><use href="#i-check"/></svg>' + scene.insight + '</div>';
    if (!paused && !focus && typeof messages.animate === 'function') {
      messages.getAnimations().forEach(animation => animation.cancel());
      messages.animate([{ opacity: 0, transform: 'translateY(7px)' }, { opacity: 1, transform: 'translateY(0)' }], { duration: 250, easing: 'ease-out' });
    }
    if (focus) tabs[index].focus();
  }
  tabs.forEach((tab, index) => tab.addEventListener('click', () => selectScene(index)));
  document.querySelector('.demo-tabs').addEventListener('keydown', event => {
    let next = currentScene;
    if (event.key === 'ArrowRight' || event.key === 'ArrowDown') next = (next + 1) % tabs.length;
    else if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') next = (next + tabs.length - 1) % tabs.length;
    else if (event.key === 'Home') next = 0;
    else if (event.key === 'End') next = tabs.length - 1;
    else return;
    event.preventDefault();
    selectScene(next, true);
  });

  let width = 0;
  let height = 0;
  let density = 1;
  const particles = Array.from({ length: 55 }, (_, index) => ({
    x: ((index * 371) % 997) / 997,
    y: ((index * 227) % 991) / 991,
    size: index % 7 === 0 ? 1.4 : 0.6,
    speed: 0.12 + (index % 5) * 0.06
  }));
  function resizeCanvas() {
    if (!context) return;
    width = canvas.clientWidth;
    height = canvas.clientHeight;
    density = Math.min(window.devicePixelRatio || 1, 1.5);
    canvas.width = Math.round(width * density);
    canvas.height = Math.round(height * density);
    context.setTransform(density, 0, 0, density, 0, 0);
    drawSignals(drawTime);
  }
  function pathPoint(t, offset) {
    const mobile = width < 650;
    const x = width * (-0.05 + 1.2 * t);
    const y = height * (mobile ? 0.81 : 0.91) - height * (mobile ? 0.38 : 0.75) * t + Math.sin(t * Math.PI * 1.9 + offset) * height * 0.095;
    return { x, y };
  }
  function drawSignals(time) {
    if (!context || !width || !height) return;
    context.clearRect(0, 0, width, height);
    const glow = context.createRadialGradient(width * 0.72, height * 0.53, 0, width * 0.72, height * 0.53, width * 0.5);
    glow.addColorStop(0, 'rgba(25,90,197,0.24)');
    glow.addColorStop(1, 'rgba(5,8,14,0)');
    context.fillStyle = glow;
    context.fillRect(0, 0, width, height);
    for (let ribbon = 0; ribbon < 5; ribbon++) {
      context.beginPath();
      for (let step = 0; step <= 90; step++) {
        const point = pathPoint(step / 90, ribbon * 0.13);
        if (step === 0) context.moveTo(point.x, point.y);
        else context.lineTo(point.x, point.y);
      }
      context.strokeStyle = ribbon === 2 ? 'rgba(147,214,255,.6)' : 'rgba(70,133,255,.23)';
      context.lineWidth = ribbon === 2 ? 1.5 : 0.8;
      context.shadowColor = '#348dff';
      context.shadowBlur = ribbon === 2 ? 19 : 9;
      context.stroke();
      context.shadowBlur = 0;
      const position = ((time * 0.000045) + ribbon * 0.2) % 1;
      const point = pathPoint(position, ribbon * 0.13);
      context.beginPath();
      context.arc(point.x, point.y, ribbon === 2 ? 2 : 1.2, 0, Math.PI * 2);
      context.fillStyle = '#9ed4ff';
      context.shadowColor = '#448bff';
      context.shadowBlur = 18;
      context.fill();
      context.shadowBlur = 0;
    }
    particles.forEach(particle => {
      const x = particle.x * width;
      const y = ((particle.y + time * particle.speed * 0.00001) % 1) * height;
      context.beginPath();
      context.arc(x, y, particle.size, 0, Math.PI * 2);
      context.fillStyle = 'rgba(130,181,248,.34)';
      context.fill();
    });
  }
  function tick(time) {
    frame = 0;
    if (paused || document.hidden || !heroVisible) return;
    if (time - previousFrame > 32) {
      drawTime += Math.min(time - previousFrame, 50);
      previousFrame = time;
      drawSignals(drawTime);
    }
    frame = requestAnimationFrame(tick);
  }
  function startCanvas() {
    if (context && !frame && !paused && !document.hidden && heroVisible) {
      previousFrame = performance.now();
      frame = requestAnimationFrame(tick);
    }
  }
  if (context) {
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas, { passive: true });
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(entries => {
        heroVisible = entries[0].isIntersecting;
        if (heroVisible) startCanvas();
        else { cancelAnimationFrame(frame); frame = 0; }
      }).observe(canvas);
    }
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) { cancelAnimationFrame(frame); frame = 0; }
      else startCanvas();
    });
  }
  const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)');
  let pointerFrame = 0;
  document.querySelector('.hero').addEventListener('pointermove', event => {
    if (paused || !finePointer.matches || window.innerWidth < 901 || !dashboard || pointerFrame) return;
    const x = event.clientX / window.innerWidth - 0.5;
    const y = event.clientY / window.innerHeight - 0.5;
    pointerFrame = requestAnimationFrame(() => {
      dashboard.style.transform = 'rotateY(' + (-18 + x * 4) + 'deg) rotateX(' + (12 - y * 3) + 'deg) rotateZ(-7deg)';
      pointerFrame = 0;
    });
  }, { passive: true });
  document.querySelector('.hero').addEventListener('pointerleave', () => { if (dashboard && !paused && window.innerWidth > 900) dashboard.style.transform = baseTransform; });
  const progress = document.querySelector('.page-progress');
  let scrollFrame = 0;
  window.addEventListener('scroll', () => {
    if (scrollFrame) return;
    scrollFrame = requestAnimationFrame(() => {
      const max = document.documentElement.scrollHeight - window.innerHeight;
      progress.style.transform = 'scaleX(' + (max > 0 ? window.scrollY / max : 0) + ')';
      scrollFrame = 0;
    });
  }, { passive: true });

  const form = document.getElementById('diagnostic-form');
  const note = document.getElementById('diagnostic-note');
  const submit = form.querySelector('[type="submit"]');
  let submitting = false;
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (submitting || !form.reportValidity()) return;
    const data = new FormData(form);
    const phone = String(data.get('whatsapp') || '').replace(/\D/g, '');
    if (phone.length < 10 || phone.length > 13) {
      note.textContent = 'Confira seu WhatsApp e inclua o DDD.';
      note.dataset.state = 'error';
      form.elements.whatsapp.focus();
      return;
    }
    const params = new URLSearchParams(window.location.search);
    let stored = {};
    try { stored = JSON.parse(sessionStorage.getItem('sp3_origem_v1') || '{}'); } catch { /* Optional attribution storage. */ }
    const payload = {
      sentAt: new Date().toISOString(),
      name: String(data.get('name') || '').trim(),
      whatsapp: String(data.get('whatsapp') || '').trim(),
      email: String(data.get('email') || '').trim(),
      volume: data.get('volume'), team: data.get('team'), pain: data.get('pain'),
      consent: data.get('consent') === 'on',
      company_website: String(data.get('company_website') || ''),
      landingPage: window.location.origin + window.location.pathname
    };
    ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'gclid', 'fbclid'].forEach(key => {
      payload[key] = String(stored[key] || params.get(key) || '').slice(0, 200);
    });
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({ event: 'diagnostic_form_submit', lead_volume: data.get('volume') });
    submitting = true;
    submit.disabled = true;
    submit.textContent = 'Enviando solicitação...';
    note.textContent = 'Aguarde enquanto enviamos sua solicitação.';
    delete note.dataset.state;
    const controller = new AbortController();
    const timeout = window.setTimeout(() => controller.abort(), 20000);
    try {
      const response = await fetch('/api/diagnostic', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload), signal: controller.signal
      });
      const result = await response.json();
      if (!response.ok || result.ok !== true) throw new Error('Submission not confirmed');
      note.textContent = 'Solicitação enviada. Nossa equipe vai entrar em contato para conhecer sua operação.';
      note.dataset.state = 'success';
      submit.textContent = 'Solicitação enviada';
      form.reset();
      window.dataLayer.push({ event: 'diagnostic_form_success', lead_volume: payload.volume });
    } catch {
      note.textContent = 'Não foi possível confirmar o envio. Seus dados continuam preenchidos. Tente novamente em instantes.';
      note.dataset.state = 'error';
      submit.textContent = 'Tentar novamente';
      submit.disabled = false;
    } finally {
      window.clearTimeout(timeout);
      submitting = false;
    }
  });
  updateMotion();
})();
