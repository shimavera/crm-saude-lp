
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
    { title: 'Pode falar. A IA acompanha.', subtitle: 'Áudio recebido e enviado · SaúdeCRM', kind: 'audio', patient: 'Quero marcar uma avaliação, mas só consigo no fim da tarde. Vocês têm esse horário?', answer: 'Olá! Vou te ajudar a encontrar uma opção. É sua primeira visita à clínica?', insight: 'A IA entende áudios e também pode responder por áudio.' },
    { title: 'A imagem também tem contexto.', subtitle: 'Compreensão de imagem · SaúdeCRM', kind: 'image', patient: 'Vi este material da clínica. Como faço para agendar essa avaliação?', answer: 'Você enviou o material sobre avaliação inicial. Posso te ajudar com o agendamento. Qual período costuma funcionar melhor para você?', insight: 'A imagem ajuda a continuar o atendimento. A avaliação clínica fica com o profissional.' },
    { title: 'Interesse com um próximo passo.', subtitle: 'Agendamento com o profissional · SaúdeCRM', kind: 'schedule', patient: 'Prefiro à tarde. Já posso marcar?', answer: 'Vamos seguir com a avaliação. Neste exemplo, temos terça às 16h ou quinta às 17h. Qual funciona melhor para você?', insight: 'O agendamento segue a disponibilidade e as regras configuradas para a clínica.' },
    { title: 'A equipe entra com o contexto.', subtitle: 'Atendimento humano · SaúdeCRM', kind: 'team', patient: 'Quero conversar com alguém da recepção.', answer: 'Com certeza. Vou encaminhar sua conversa para a equipe continuar o atendimento com o que você já compartilhou.', insight: 'Sua recepção recebe o histórico e assume quando necessário.' }
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
    const audioWave = '<span class="audio-wave" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></span>';
    const patientLabel = scene.kind === 'audio' ? 'EXEMPLO DE ÁUDIO TRANSCRITO' : 'PACIENTE';
    const answerLabel = scene.kind === 'audio' ? 'RESPOSTA EM ÁUDIO, TRANSCRITA' : 'SAÚDECRM IA';
    const mediaCard = scene.kind === 'image' ? '<div class="demo-image-card"><span>SAÚDECRM / CLÍNICA DEMONSTRATIVA</span><strong>Avaliação inicial.</strong><small>Conheça nosso atendimento.</small><svg><use href="#i-spark"/></svg></div>' : '';
    const scheduleCard = scene.kind === 'schedule' ? '<div class="demo-appointment"><svg><use href="#i-check"/></svg><div><b>Exemplo: avaliação agendada</b><span>Dra. Sofia · quinta, 17h</span><small>Profissional e horário fictícios.</small></div></div>' : '';
    messages.innerHTML = mediaCard + '<div class="scene-message from-patient"><span>' + patientLabel + '</span>' + (scene.kind === 'audio' ? audioWave : '') + scene.patient + '</div><div class="scene-message from-ai"><span><svg><use href="#i-spark"/></svg> ' + answerLabel + '</span>' + scene.answer + '</div>' + scheduleCard + '<div class="scene-insight"><svg><use href="#i-check"/></svg>' + scene.insight + '</div>';
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


  const productScreens = [
    { name: 'Dashboard', src: '/assets/product/dashboard.jpg', alt: 'Dashboard demonstrativo do SaúdeCRM com visão geral da operação', caption: 'Sua operação organizada para acompanhar o próximo passo.' },
    { name: 'Conversas', src: '/assets/product/conversas.jpg', alt: 'Interface demonstrativa de conversas do SaúdeCRM, com histórico e atendimento da IA', caption: 'O histórico acompanha o atendimento da IA e da sua equipe.' },
    { name: 'Kanban', src: '/assets/product/kanban.jpg', alt: 'Funil demonstrativo do SaúdeCRM organizado em colunas por etapa do atendimento', caption: 'Cada contato tem uma etapa para acompanhar.' }
  ];
  const productTabs = Array.from(document.querySelectorAll('[data-product]'));
  const productImage = document.getElementById('product-image');
  const productPanel = document.getElementById('product-panel');
  let productIndex = 0;
  function selectProduct(index, focus = false) {
    productIndex = index;
    const screen = productScreens[index];
    productTabs.forEach((tab, tabIndex) => {
      tab.setAttribute('aria-selected', String(tabIndex === index));
      tab.tabIndex = tabIndex === index ? 0 : -1;
    });
    productPanel.setAttribute('aria-labelledby', productTabs[index].id);
    productImage.src = screen.src;
    productImage.alt = screen.alt;
    document.getElementById('product-caption').textContent = screen.caption;
    if (focus) productTabs[index].focus();
  }
  productTabs.forEach((tab, index) => tab.addEventListener('click', () => selectProduct(index)));
  document.querySelector('.product-tabs').addEventListener('keydown', event => {
    let next = productIndex;
    if (event.key === 'ArrowRight') next = (next + 1) % productTabs.length;
    else if (event.key === 'ArrowLeft') next = (next + productTabs.length - 1) % productTabs.length;
    else if (event.key === 'Home') next = 0;
    else if (event.key === 'End') next = productTabs.length - 1;
    else return;
    event.preventDefault();
    selectProduct(next, true);
  });
  const productDialog = document.getElementById('product-dialog');
  const dialogImage = document.getElementById('dialog-product-image');
  let dialogTrigger = null;
  document.querySelectorAll('[data-open-product]').forEach(trigger => {
    trigger.addEventListener('click', () => {
      const value = trigger.dataset.openProduct;
      const screen = productScreens[value === 'current' ? productIndex : Number(value)];
      if (!screen || !productDialog) return;
      dialogTrigger = trigger;
      document.getElementById('dialog-title').textContent = screen.name + ' SaúdeCRM';
      dialogImage.src = screen.src;
      dialogImage.alt = screen.alt + ', ampliado';
      if (typeof productDialog.showModal === 'function') {
        productDialog.showModal();
        document.body.classList.add('dialog-open');
        productDialog.querySelector('.dialog-close').focus();
      }
    });
  });
  productDialog.querySelector('.dialog-close').addEventListener('click', () => productDialog.close());
  productDialog.addEventListener('click', event => {
    if (event.target !== productDialog) return;
    const bounds = productDialog.getBoundingClientRect();
    if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) productDialog.close();
  });
  productDialog.addEventListener('close', () => {
    document.body.classList.remove('dialog-open');
    if (dialogTrigger && document.contains(dialogTrigger)) dialogTrigger.focus({ preventScroll: true });
  });
  selectScene(0);

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
  const formPanels = Array.from(form.querySelectorAll('[data-form-step]'));
  const formNext = form.querySelector('.form-next');
  const formBack = form.querySelector('.form-back');
  const formProgress = form.querySelector('.form-progress');
  const formCounter = document.querySelector('.form-counter');
  const formPanelWrap = form.querySelector('.diagnostic-panels');
  const initialNote = note.innerHTML;
  let formStep = 0;
  form.noValidate = true;
  form.classList.add('form-enhanced');
  function fieldError(name, message) {
    const error = document.getElementById(name + '-error');
    if (error) { error.textContent = message; error.hidden = !message; }
    form.querySelectorAll('[name="' + name + '"]').forEach(control => {
      if (message) control.setAttribute('aria-invalid', 'true');
      else control.removeAttribute('aria-invalid');
    });
  }
  function validateFormStep(index) {
    let firstInvalid = null;
    if (index === 0) {
      ['volume', 'team', 'pain'].forEach(name => {
        const selected = form.querySelector('[name="' + name + '"]:checked');
        fieldError(name, selected ? '' : 'Escolha uma opção para continuar.');
        if (!selected && !firstInvalid) firstInvalid = form.querySelector('[name="' + name + '"]');
      });
    } else {
      ['name', 'whatsapp', 'email', 'consent'].forEach(name => {
        const control = form.elements.namedItem(name);
        let message = '';
        if (name === 'consent' && !control.checked) message = 'Autorize o contato para enviar a solicitação.';
        else if (name !== 'consent' && !control.value.trim()) message = 'Preencha este campo para continuar.';
        else if (name === 'email' && !control.checkValidity()) message = 'Confira o e-mail informado.';
        else if (name === 'whatsapp') {
          const digits = control.value.replace(/\D/g, '');
          if (digits.length < 10 || digits.length > 13) message = 'Confira seu WhatsApp e inclua o DDD.';
        }
        fieldError(name, message);
        if (message && !firstInvalid) firstInvalid = control;
      });
    }
    if (firstInvalid) { firstInvalid.focus(); return false; }
    return true;
  }
  function measureFormPanels() {
    const width = formPanelWrap.clientWidth;
    if (!width) return;
    let height = 0;
    formPanels.forEach(panel => {
      const wasHidden = panel.hidden;
      const savedStyle = panel.getAttribute('style');
      panel.hidden = false;
      panel.style.cssText = 'position:absolute;visibility:hidden;pointer-events:none;left:0;top:0;width:' + width + 'px;';
      height = Math.max(height, panel.getBoundingClientRect().height);
      if (savedStyle === null) panel.removeAttribute('style'); else panel.setAttribute('style', savedStyle);
      panel.hidden = wasHidden;
    });
    formPanelWrap.style.minHeight = Math.ceil(height) + 'px';
  }
  function showFormStep(index, focus = false) {
    formStep = index;
    formPanels.forEach((panel, panelIndex) => { panel.hidden = panelIndex !== index; });
    formNext.hidden = index !== 0;
    formBack.hidden = index !== 1;
    submit.hidden = index !== 1;
    formProgress.hidden = false;
    formCounter.hidden = false;
    formCounter.textContent = index === 0 ? '01 / 02' : '02 / 02';
    formProgress.setAttribute('aria-label', 'Etapa ' + (index + 1) + ' de 2');
    formProgress.querySelectorAll('.form-progress-step').forEach((step, stepIndex) => {
      step.classList.toggle('is-current', stepIndex === index);
      step.classList.toggle('is-complete', stepIndex < index);
      if (stepIndex === index) step.setAttribute('aria-current', 'step');
      else step.removeAttribute('aria-current');
    });
    form.querySelector('.form-answer-summary').hidden = index !== 1;
    if (focus) {
      const heading = formPanels[index].querySelector('h3');
      heading.tabIndex = -1;
      heading.focus({ preventScroll: true });
    }
    measureFormPanels();
  }
  formNext.addEventListener('click', () => {
    if (validateFormStep(0)) { note.innerHTML = initialNote; delete note.dataset.state; showFormStep(1, true); }
    else measureFormPanels();
  });
  formBack.addEventListener('click', () => {
    if (!submitting) { note.innerHTML = initialNote; delete note.dataset.state; showFormStep(0, true); }
  });
  form.addEventListener('input', event => {
    if (event.target.name && event.target.getAttribute('aria-invalid')) fieldError(event.target.name, '');
  });
  form.addEventListener('change', event => {
    if (event.target.type === 'radio') fieldError(event.target.name, '');
  });
  showFormStep(0);
  window.addEventListener('resize', measureFormPanels, { passive: true });
  if (document.fonts) document.fonts.ready.then(measureFormPanels);
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (submitting) return;
    if (formStep === 0) {
      if (validateFormStep(0)) showFormStep(1, true);
      else measureFormPanels();
      return;
    }
    if (!validateFormStep(1)) { measureFormPanels(); return; }
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
    formBack.disabled = true;
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
      formBack.disabled = false;
    } finally {
      window.clearTimeout(timeout);
      submitting = false;
    }
  });
  updateMotion();
})();
