(() => {
  'use strict';

  if (window.__bridgeInteractionHostReady) return;
  window.__bridgeInteractionHostReady = true;

  const hostTag = 'bridge-interaction-host';
  const learningTag = 'bridge-learning-cycle';
  const shellTag = 'bridge-interaction-shell';
  const frames = [];
  const studioFiles = new Set([
    '03-reaction-bridge-3d.html',
    'arch-bridge-hybrid-fem.html',
    'bridge-shell-mitc4.html'
  ]);

  const frameFile = (iframe) => {
    try { return new URL(iframe.src, location.href).pathname.split('/').pop() || ''; }
    catch (_) { return ''; }
  };
  const classifyLayout = (iframe) => {
    if (iframe.dataset.layout === 'studio' || iframe.dataset.layout === 'flow') {
      return iframe.dataset.layout;
    }
    return studioFiles.has(frameFile(iframe)) ? 'studio' : 'flow';
  };
  const post = (meta, type, payload = {}) => {
    if (!meta.iframe.contentWindow) return;
    meta.iframe.contentWindow.postMessage({ source: hostTag, type, ...payload }, '*');
  };
  const metaForSource = (source) => frames.find((meta) => meta.iframe.contentWindow === source);

  function createToolbar(meta) {
    const toolbar = document.createElement('div');
    toolbar.className = 'interaction-toolbar';
    toolbar.dataset.interactionHostOwned = 'true';
    const label = document.createElement('div');
    label.className = 'interaction-toolbar__title';
    const eyebrow = document.createElement('span');
    eyebrow.textContent = meta.layout === 'studio' ? '可转动模型' : '动手试试';
    const title = document.createElement('strong');
    title.textContent = meta.iframe.title || '交互实验';
    label.append(eyebrow, title);

    const actions = document.createElement('div');
    actions.className = 'interaction-toolbar__actions';
    const open = document.createElement('a');
    open.className = 'interaction-toolbar__link';
    open.href = meta.iframe.getAttribute('src') || meta.iframe.src;
    open.target = '_blank';
    open.rel = 'noopener';
    open.textContent = '单独打开 ↗';
    open.setAttribute('aria-label', `在新窗口打开：${meta.iframe.title || '交互实验'}`);
    actions.appendChild(open);

    if (document.fullscreenEnabled) {
      const fullscreen = document.createElement('button');
      fullscreen.type = 'button';
      fullscreen.className = 'interaction-toolbar__fullscreen';
      fullscreen.textContent = '全屏';
      fullscreen.addEventListener('click', async () => {
        try {
          if (document.fullscreenElement === meta.block) await document.exitFullscreen();
          else await meta.block.requestFullscreen();
        } catch (_) {}
      });
      meta.fullscreen = fullscreen;
      actions.appendChild(fullscreen);
    }
    toolbar.append(label, actions);
    meta.toolbar = toolbar;
    meta.block.insertBefore(toolbar, meta.iframe);
  }

  function renderLearningHost(meta, lesson, initialState) {
    if (!meta.learning) {
      const questionMount = document.createElement('div');
      const resultMount = document.createElement('div');
      questionMount.className = 'learning-cycle-flow-mount learning-cycle-flow-mount--question interaction-learning-host';
      resultMount.className = 'learning-cycle-flow-mount learning-cycle-flow-mount--result interaction-learning-host';
      questionMount.dataset.interactionHostOwned = 'true';
      resultMount.dataset.interactionHostOwned = 'true';
      questionMount.innerHTML = `
        <section class="learning-cycle-panel learning-cycle-panel--question" aria-label="操作前的判断">
          <div class="learning-cycle-datum"><span>猜</span>先猜一句</div>
          <h2 class="learning-cycle-question"></h2>
          <p class="learning-cycle-task"><strong>这次只改：</strong><span></span></p>
          <label class="learning-cycle-label">你觉得会怎样？</label>
          <textarea class="learning-cycle-before" rows="2" placeholder="写一句就行。"></textarea>
          <div class="learning-cycle-actions">
            <button type="button" class="learning-cycle-start">留下判断</button>
            <span class="learning-cycle-progress" aria-live="polite"></span>
          </div>
        </section>`;
      resultMount.innerHTML = `
        <section class="learning-cycle-panel learning-cycle-panel--result" aria-label="操作后的解释">
          <div class="learning-cycle-datum"><span>看</span>动手以后</div>
          <label class="learning-cycle-label">哪一处变化最能说明问题？</label>
          <textarea class="learning-cycle-revise" rows="2" placeholder="引用一个画面、数值或趋势。"></textarea>
          <div class="learning-cycle-result-progress" aria-live="polite"></div>
          <div class="learning-cycle-principle" aria-live="polite">
            <div class="learning-cycle-gate"></div>
            <div class="learning-cycle-reveal" hidden>
              <h3>刚才看到的规律</h3><p class="learning-cycle-term"></p>
              <h3>这招还能用在哪儿</h3><p class="learning-cycle-transfer"></p>
            </div>
          </div>
        </section>`;
      meta.block.insertBefore(questionMount, meta.toolbar);
      meta.iframe.insertAdjacentElement('afterend', resultMount);

      const ui = {
        questionMount,
        resultMount,
        question: questionMount.querySelector('.learning-cycle-question'),
        task: questionMount.querySelector('.learning-cycle-task span'),
        before: questionMount.querySelector('.learning-cycle-before'),
        start: questionMount.querySelector('.learning-cycle-start'),
        progress: questionMount.querySelector('.learning-cycle-progress'),
        revise: resultMount.querySelector('.learning-cycle-revise'),
        resultProgress: resultMount.querySelector('.learning-cycle-result-progress'),
        gate: resultMount.querySelector('.learning-cycle-gate'),
        reveal: resultMount.querySelector('.learning-cycle-reveal'),
        term: resultMount.querySelector('.learning-cycle-term'),
        transfer: resultMount.querySelector('.learning-cycle-transfer')
      };
      ui.before.addEventListener('input', () => post(meta, 'command', { command: 'set-before', value: ui.before.value }));
      ui.revise.addEventListener('input', () => post(meta, 'command', { command: 'set-revise', value: ui.revise.value }));
      ui.start.addEventListener('click', () => post(meta, 'command', { command: 'start' }));
      meta.learning = ui;
    }

    const ui = meta.learning;
    ui.question.textContent = lesson.question;
    ui.task.textContent = lesson.task;
    ui.term.textContent = lesson.term;
    ui.transfer.textContent = lesson.transfer;
    updateLearningHost(meta, initialState);
  }

  function updateLearningHost(meta, state = {}) {
    const ui = meta.learning;
    if (!ui) return;
    const beforeText = state.before || '';
    const reviseText = state.revise || '';
    const evidence = Number.isFinite(state.evidence) ? state.evidence : 0;
    if (document.activeElement !== ui.before) ui.before.value = beforeText;
    if (document.activeElement !== ui.revise) ui.revise.value = reviseText;
    ui.start.disabled = beforeText.trim().length < 2;
    ui.start.textContent = state.started ? '更新判断' : '留下判断';
    ui.progress.textContent = state.started ? `已记录 · 对照 ${evidence}/2` : '先留下判断，再操作';
    ui.resultProgress.textContent = state.started
      ? `已经比较 ${evidence}/2 个状态`
      : '上面的判断留下后，这里才开始记录对照。';
    ui.reveal.hidden = !state.ready;
    ui.gate.hidden = Boolean(state.ready);
    if (!state.started) ui.gate.textContent = '先在上面留下一句判断。';
    else if (evidence < 2) ui.gate.textContent = '再改变一次同一个控制量，比较两个状态。';
    else if (!state.reflected) ui.gate.textContent = '把你看见的变化写成一句话，再看背后的关系。';
  }

  function applyFlowHeight(meta, rawHeight) {
    if (meta.layout !== 'flow') return;
    const height = Math.max(360, Math.min(7000, Math.ceil(Number(rawHeight) || 0)));
    if (!height || Math.abs(height - meta.currentHeight) < 5) return;
    meta.currentHeight = height;
    meta.iframe.style.height = `${height}px`;
  }

  function attachSameOriginObserver(meta) {
    if (meta.layout !== 'flow') return;
    if (meta.resizeObserver) meta.resizeObserver.disconnect();
    try {
      const doc = meta.iframe.contentDocument;
      if (!doc || !doc.documentElement || !doc.body) return;
      const measure = () => {
        const root = doc.documentElement;
        const body = doc.body;
        applyFlowHeight(meta, Math.max(root.scrollHeight, root.offsetHeight, body.scrollHeight, body.offsetHeight));
      };
      if ('ResizeObserver' in window) {
        const observer = new ResizeObserver(measure);
        observer.observe(doc.documentElement);
        observer.observe(doc.body);
        meta.resizeObserver = observer;
      }
      measure();
    } catch (_) {}
  }

  function enhanceBlock(block) {
    if (block.dataset.interactionHostEnhanced === 'true') return;
    const iframe = block.querySelector('iframe');
    if (!iframe) return;
    block.dataset.interactionHostEnhanced = 'true';
    block.classList.add('interactive-block--enhanced', 'interactive-block--wide');
    const declaredLayout = ['studio', 'flow'].includes(iframe.dataset.layout)
      ? iframe.dataset.layout
      : (['studio', 'flow'].includes(block.dataset.layout) ? block.dataset.layout : '');
    const layout = declaredLayout || classifyLayout(iframe);
    block.classList.add(`interactive-block--${layout}`);
    iframe.dataset.layout = layout;
    iframe.setAttribute('scrolling', layout === 'flow' ? 'no' : 'auto');
    const fallbackHeight = Number.parseInt(iframe.getAttribute('height') || '720', 10);
    const meta = { block, iframe, layout, declaredLayout, currentHeight: fallbackHeight };
    frames.push(meta);
    createToolbar(meta);
    iframe.addEventListener('load', () => {
      post(meta, 'request-init');
      attachSameOriginObserver(meta);
    });
    if (iframe.contentDocument && iframe.contentDocument.readyState !== 'loading') {
      post(meta, 'request-init');
      attachSameOriginObserver(meta);
    }
  }

  window.addEventListener('message', (event) => {
    const message = event.data || {};
    if (message.source !== learningTag && message.source !== shellTag) return;
    const meta = metaForSource(event.source);
    if (!meta) return;
    if (message.source === shellTag && message.type === 'resize') {
      if (!meta.declaredLayout && (message.layout === 'flow' || message.layout === 'studio')) {
        meta.layout = message.layout;
      }
      applyFlowHeight(meta, message.height);
      return;
    }
    if (message.source === learningTag && message.type === 'init' && message.lesson) {
      renderLearningHost(meta, message.lesson, message.state || {});
      post(meta, 'mount');
      return;
    }
    if (message.source === learningTag && message.type === 'state') {
      updateLearningHost(meta, message.state || {});
    }
  });

  document.addEventListener('fullscreenchange', () => {
    frames.forEach((meta) => {
      if (meta.fullscreen) meta.fullscreen.textContent = document.fullscreenElement === meta.block ? '退出全屏' : '全屏';
    });
  });

  const scan = () => document.querySelectorAll('.interactive-block').forEach(enhanceBlock);
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', scan, { once: true });
  else scan();
})();
