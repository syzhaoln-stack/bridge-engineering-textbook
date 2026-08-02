(() => {
  'use strict';

  const file = location.pathname.split('/').pop() || '';
  const query = new URLSearchParams(location.search);
  const mode = query.get('mode') || query.get('type') || '';
  const id = mode ? `${file}?${mode}` : file;

  const lessons = {
    '03-load-budget.html': {
      question: '一座桥比一辆车重几百倍，能不能据此说它一定很安全？',
      task: '先写下“桥自身重量 : 交通重量”的大致比例，再改变车辆数。注意比例变化与承载能力并不是同一件事。',
      term: '恒载占比、活载储备、承载能力是三件相连但不能互换的事。',
      transfer: '换成长跨悬索桥：主缆和加劲梁都更轻时，活载占比会怎样变化？还缺什么证据才能谈安全？'
    },
    '03-reaction-bridge-3d.html': {
      question: '车还没到跨中以前，远端支座会不会已经“感觉到”它？',
      task: '让车从左向右走，不盯数字，只看两端反力柱怎样此消彼长。把车停在你认为两端刚好平分的位置。',
      term: '整体平衡不是等车走到某个构件上才开始；支座反力随荷载位置连续重分配。',
      transfer: '若右端支座突然失效，原来的反力要从哪条新路径回到地面？'
    },
    '04-where-to-park.html': {
      question: '同一辆车，想让右支座最吃力和想让跨中最吃力，应当停在同一处吗？',
      task: '先分别停车两次，再打开曲线核对。不要拖着车寻找数字峰值，要先凭结构判断停一次。',
      term: '“最不利位置”必须连着一个明确响应；影响线固定观察量，让荷载移动。',
      transfer: '把观察对象换成桥面悬臂板根部，车的位置又应怎样改变？'
    },
    '04-continuous-loading.html': {
      question: '为了让中支点负弯矩最大，把两跨全部塞满车真的最坏吗？',
      task: '先自己布置一遍，再显示有利区。比较你多放了哪一段、少放了哪一段。',
      term: '连续梁影响线会变号；荷载放在同号区才会把目标响应推向同一方向。',
      transfer: '若目标改成左跨跨中正弯矩，刚才的车队中哪一部分会从“帮忙”变成“拆台”？'
    },
    '04-transverse-share.html': {
      question: '车靠最右侧时，左侧主梁会不会完全不受力？',
      task: '先遮住百分比，只看桥面与主梁的变形关系；再移动轮载，观察横向构件怎样把力送到远侧。',
      term: '横向分布不是平均分，也不是最近者独占；它由桥面板、横隔梁、主梁与扭转刚度共同决定。',
      transfer: '若把两片梁换成闭口箱梁，偏载还会额外激起哪一种整体作用？'
    },
    'fundamentals-lab.html?crossing': {
      question: '河宽没有变，路线只斜了一点，桥长为什么可能接近翻倍？',
      task: '先在纸上估计 45° 和 30° 时的长度，再调角度核对。找出“角度开始昂贵”的区间。',
      term: '这是斜交跨越的平面几何；它先改变实际跨越长度，随后才把代价传给结构和施工。',
      transfer: '机场滑行道与车行通道斜交时，除了结构长度，还会改变哪一项净空布置？'
    },
    'fundamentals-lab.html?scale': {
      question: '所有尺寸都放大两倍，自重弯矩和名义抗弯能力谁跑得更快？',
      task: '先写两个倍率，再把比例从 1 推到 5。不要只看终点，留意两条曲线为何越走越开。',
      term: '几何相似放大时，自重弯矩约按四次方增长，截面抗弯能力约按三次方增长。',
      transfer: '蜘蛛侠、恐龙和高层建筑为什么都不能只把小尺度方案等比例放大？'
    },
    'fundamentals-lab.html?forcepath': {
      question: '一根构件删掉以后外形还像桥，为什么它可能已经不是一座能工作的桥？',
      task: '换三种桥型，各删一次连接。沿亮起的路线追到地基，找出第一处断掉的交接。',
      term: '几何接触不等于力学连接；完整力路必须把荷载连续送到基础，并满足接口平衡。',
      transfer: '在组织或软件系统里，哪一种“看起来连上了”的接口也可能实际不传递任务？'
    },
    'fundamentals-lab.html?curve': {
      question: '一条索看起来是抛物线，是否说明它在任何荷载下都愿意保持抛物线？',
      task: '先换荷载分布，再比较曲线。分清“画出来的形”与“在这组荷载下的平衡形”。',
      term: '合理形状由荷载分布、边界和水平分力共同决定；同形不等于同一受力问题。',
      transfer: '拱桥把索的受拉翻成受压以后，形状判断还要多检查什么？'
    },
    'bridge-systems-atlas.html?beam': {
      question: '把梁高加倍，弯矩图会不会跟着减半？',
      task: '先只改梁高，再只改跨度。分别观察弯矩图和变形，找出“荷载效应”与“刚度响应”的区别。',
      term: '线性静定梁的弯矩主要由荷载与几何平衡决定；梁高通过截面惯性矩强烈改变应力和挠度。',
      transfer: '若改成连续梁，梁高变化会不会进一步改变各跨弯矩分配？'
    },
    'bridge-systems-atlas.html?supports': {
      question: '同样升温 30℃，桥能自由伸长和两端锁死，肉眼变形可能都不大，内力会一样吗？',
      task: '在“可动”和“锁死”之间切换。先看位移，再看约束力；说明哪一种结果更容易被照片漏掉。',
      term: '边界释放把温度变化转成位移；边界锁定则把它转成约束内力。',
      transfer: '混凝土收缩、基础沉降和预应力张拉中，哪里也存在“允许动还是不允许动”的同类问题？'
    },
    'bridge-systems-atlas.html?construction': {
      question: '左右只差一个悬臂节段，为什么墩顶会像被人用扳手拧住？',
      task: '先保持两侧对称，再让一侧多一个节段。观察不平衡力矩从哪里出现、由谁临时承担。',
      term: '施工阶段有自己的结构体系；成桥平衡不能倒推每一个中间状态都安全。',
      transfer: '斜拉桥单侧挂索、悬索桥主缆架设时，哪一个“尚未闭合”的状态最值得单独算？'
    },
    'bridge-systems-atlas.html?beauty': {
      question: '一座桥显得“别扭”，究竟是个人口味，还是眼睛读到了不可信的受力比例？',
      task: '先盲调到你觉得顺眼，再显示塔、梁、索的力学提示。记录哪一个比例最先改变了判断。',
      term: '结构可读性可以参与审美判断，但效率并不是美的充分条件。',
      transfer: '找一座你不喜欢却受力清楚的桥，再找一座你喜欢但力路被隐藏的桥；分别说明理由。'
    },
    'long-span-load-path.html?suspension': {
      question: '吊杆把车重交给主缆以后，主缆的巨大水平分力最后由谁接住？',
      task: '从一只车轮追到锚碇，随后隐藏锚碇。观察外形仍像悬索桥时，力路在哪一步失去出口。',
      term: '地锚式悬索桥用锚碇平衡主缆水平分力；主塔主要接收竖向分量。',
      transfer: '自锚式悬索桥没有地锚时，水平分力改由哪个构件闭合？施工次序为什么随之改变？'
    },
    'long-span-load-path.html?cable': {
      question: '只在主跨一侧加车，桥塔两边的拉索还能互相抵消吗？',
      task: '改变车辆位置和索力基准，比较塔两侧索力条。先找“不平衡”，再看主梁轴压和塔弯矩的回应。',
      term: '斜拉桥是拉索、受压桥塔和受弯压主梁的组合体系；不对称荷载会打破塔两侧平衡。',
      transfer: '边跨长度变短却不加压重时，哪一种不平衡可能先控制设计？'
    },
    'arch-bridge-hybrid-fem.html': {
      question: '轮载从拱顶移到四分之一跨，哪一侧拱脚会先多接到力？拱内只剩压力吗？',
      task: '先凭对称性停车一次，再移动轴列。比较拱脚反力、拱肋轴力和弯矩，不要只看一张云图。',
      term: '拱在接近合理轴线时以受压为主；不对称活载会显著引入弯曲与反力重分配。',
      transfer: '若一侧拱脚发生小量沉降，哪一种内力会最先偏离原来的对称状态？'
    },
    'bridge-fem-hierarchy.html': {
      question: '整体挠度、轮载横向分配和孔边局部应力，能不能交给同一个“最精细”模型回答？',
      task: '依次切换线梁、梁格、壳和混合模型。每换一次，只写它新回答了什么、又多要了什么输入。',
      term: '模型层级不是逼真度排名；选择模型是在问题、保留机制、输入成本和验证能力之间取舍。',
      transfer: '若只想比较两个方案的整体刚度，为什么实体模型反而可能让判断变慢？'
    },
    'bridge-shell-mitc4.html': {
      question: '车辆横移半个车道，整体总反力不变，桥面最危险的位置会不会改变？',
      task: '固定色标，先沿纵向移动，再横向偏载。比较板、横梁和主梁附近的响应，不要让每帧自动换色骗过眼睛。',
      term: '总平衡不变并不等于局部分配不变；板壳模型用双向弯曲与横向剪切表达轮载扩散。',
      transfer: '若把轮载施加成数学点而不设接触面积，网格加密时局部峰值会怎样？'
    },
    'modeling-lab.html?wind': {
      question: '风速翻倍，桥的响应一定只翻四倍吗？什么时候会突然比四倍大得多？',
      task: '先验证风力的平方关系，再把频率比推近 1、降低阻尼。把“输入变大”和“系统放大”分开。',
      term: '平均气动力约随风速平方变化；动力响应还受频率匹配、阻尼和反馈稳定控制。',
      transfer: '看到桥振动视频时，至少还需要哪两种数据，才能区分抖振、涡振和颤振？'
    },
    'modeling-lab.html?fem': {
      question: '一张云图非常平滑、网格也很细，能不能说明结果可信？',
      task: '故意漏自重、锁死转角或改变网格。按“最便宜的检查”依次看变形方向、总反力、闭式解和网格趋势。',
      term: '验证不是继续算得更复杂，而是让模型通过平衡、基准解、参数趋势和独立证据的交叉检查。',
      transfer: '若两个软件结果完全一致，却用了同一组错误边界，为什么仍可能一起错？'
    },
    'decision-evidence-lab.html?choice': {
      question: '跨度已经足够大，技术上能建斜拉桥，是否就应该选斜拉桥？',
      task: '先写一个你偏爱的桥型，再逐条放入净空、地基、施工和维护约束。记录是哪条证据让它退出。',
      term: '桥型比选先过硬约束，再比较全寿命代价与价值；技术可行只是候选资格。',
      transfer: '把桥型换成软件、设备或职业选择：你的“退出条件”是什么？'
    },
    'decision-evidence-lab.html?durability': {
      question: '同样宽的裂缝，为什么一条十年没事，另一条可能很快锈蚀？',
      task: '一次只改环境、保护层或检查间隔。沿水和氯离子的路线，找出最先失守的一环。',
      term: '耐久是裂缝—环境—传输—腐蚀—维护组成的时间链，不由单一裂缝宽度决定。',
      transfer: '若排水孔堵塞，为什么一个很小的构造问题会改变整条耐久链？'
    },
    'decision-evidence-lab.html?failure': {
      question: '事故照片里最醒目的裂缝，是原因、结果，还是两者都不是？',
      task: '不要给原因投票。先按“哪条证据最能排除一种解释”安排调查顺序，并保留未知项。',
      term: '事故分析使用竞争性假设和证据链；照片是观测，不自动等于因果。',
      transfer: '面对一次软件故障或医疗症状，怎样避免把最醒目的现象直接当根因？'
    },
    'decision-evidence-lab.html?defense': {
      question: '你最喜欢的方案，需要出现哪一条证据，你才愿意放弃它？',
      task: '保存第一版，只改一个主要参数。说明这次修改改变了哪条力路、哪个施工状态或哪项维护条件。',
      term: '设计辩护不是证明自己一开始就对，而是让目标、证据、修改和退出条件可追踪。',
      transfer: '把方案交给没参与设计的人：他能否仅凭一张图指出你的关键假设？'
    }
  };

  const lesson = lessons[id];
  if (!lesson || window.__bridgeLearningCycleReady) return;
  window.__bridgeLearningCycleReady = true;

  const scriptUrl = document.currentScript && document.currentScript.src
    ? document.currentScript.src
    : location.href;
  if (!document.querySelector('link[data-learning-cycle-style]')) {
    const stylesheet = document.createElement('link');
    stylesheet.rel = 'stylesheet';
    stylesheet.href = new URL('./learning-cycle.css', scriptUrl).href;
    stylesheet.dataset.learningCycleStyle = 'true';
    document.head.appendChild(stylesheet);
  }

  const sourceTag = 'bridge-learning-cycle';
  const hostTag = 'bridge-interaction-host';
  const shellTag = 'bridge-interaction-shell';
  const storageKey = `bridge-learning-cycle:v3:${id}`;
  const legacyKey = `bridge-learning-cycle:v2:${id}`;
  const embedded = window.parent !== window;
  const initialStates = new Map();
  const stateListeners = new Set();
  let hosted = false;
  let standalone = null;

  const readStored = (key) => {
    try { return JSON.parse(localStorage.getItem(key) || '{}'); } catch (_) { return {}; }
  };
  const storedV3 = readStored(storageKey);
  const saved = Object.keys(storedV3).length ? storedV3 : readStored(legacyKey);
  let beforeText = typeof saved.before === 'string' ? saved.before : '';
  let reviseText = typeof saved.revise === 'string' ? saved.revise : '';
  let started = Boolean(saved.started && beforeText.trim());
  const stateHistory = new Map(
    Object.entries(saved.stateHistory || {}).map(([key, values]) => [
      key,
      new Set(Array.isArray(values) ? values : [])
    ])
  );

  const evidenceCount = () => Math.min(
    2,
    Math.max(0, ...[...stateHistory.values()].map((values) => values.size))
  );
  const statePayload = () => ({
    id,
    before: beforeText,
    revise: reviseText,
    started,
    evidence: evidenceCount(),
    reflected: reviseText.trim().length >= 4,
    ready: started && evidenceCount() >= 2 && reviseText.trim().length >= 4
  });
  const persist = () => {
    const serialHistory = Object.fromEntries(
      [...stateHistory].map(([key, values]) => [key, [...values]])
    );
    try {
      localStorage.setItem(storageKey, JSON.stringify({
        before: beforeText,
        revise: reviseText,
        started,
        stateHistory: serialHistory
      }));
    } catch (_) {}
  };
  const postToParent = (type, payload = {}) => {
    if (!embedded) return;
    window.parent.postMessage({ source: sourceTag, type, id, ...payload }, '*');
  };
  const notifyState = () => {
    const state = statePayload();
    stateListeners.forEach((listener) => listener(state));
    postToParent('state', { state });
  };

  const controlKey = (element) => {
    const type = element.getAttribute('type') || element.tagName.toLowerCase();
    const parent = element.closest('[id]');
    const name = element.id
      || element.getAttribute('name')
      || element.dataset.key
      || element.dataset.v
      || element.dataset.mode
      || element.getAttribute('aria-label')
      || element.textContent.trim().slice(0, 28);
    return `${type}:${parent && parent !== element ? `${parent.id}:` : ''}${name || 'anonymous'}`;
  };
  const controlState = (element) => {
    if (element.matches('input[type="checkbox"],input[type="radio"]')) {
      return `${element.value}:${element.checked}`;
    }
    if (element.matches('input,select,textarea')) return String(element.value);
    return `active:${element.classList.contains('active')}|pressed:${element.getAttribute('aria-pressed') || ''}|expanded:${element.getAttribute('aria-expanded') || ''}`;
  };
  const eligibleControls = () => [...document.querySelectorAll('input,select,button,[role="button"]')]
    .filter((element) => !element.disabled && !element.closest('[data-learning-cycle-owned]'));
  const snapshotInitialStates = () => {
    eligibleControls().forEach((element) => initialStates.set(controlKey(element), controlState(element)));
  };
  const addEvidence = (element) => {
    if (!started) return;
    const key = controlKey(element);
    const values = stateHistory.get(key) || new Set();
    const initial = initialStates.get(key);
    if (initial != null) values.add(initial);
    values.add(controlState(element));
    stateHistory.set(key, values);
    persist();
    notifyState();
  };

  const applyCommand = (command, value) => {
    if (command === 'set-before') beforeText = String(value || '');
    if (command === 'set-revise') reviseText = String(value || '');
    if (command === 'start' && beforeText.trim().length >= 2) {
      started = true;
      snapshotInitialStates();
    }
    persist();
    notifyState();
  };

  function renderLearningUI(questionMount, resultMount, dispatch) {
    questionMount.dataset.learningCycleOwned = 'true';
    resultMount.dataset.learningCycleOwned = 'true';
    questionMount.classList.add('learning-cycle-flow-mount', 'learning-cycle-flow-mount--question');
    resultMount.classList.add('learning-cycle-flow-mount', 'learning-cycle-flow-mount--result');
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

    const question = questionMount.querySelector('.learning-cycle-question');
    const task = questionMount.querySelector('.learning-cycle-task span');
    const before = questionMount.querySelector('.learning-cycle-before');
    const start = questionMount.querySelector('.learning-cycle-start');
    const progress = questionMount.querySelector('.learning-cycle-progress');
    const revise = resultMount.querySelector('.learning-cycle-revise');
    const resultProgress = resultMount.querySelector('.learning-cycle-result-progress');
    const gate = resultMount.querySelector('.learning-cycle-gate');
    const reveal = resultMount.querySelector('.learning-cycle-reveal');
    const term = resultMount.querySelector('.learning-cycle-term');
    const transfer = resultMount.querySelector('.learning-cycle-transfer');
    question.textContent = lesson.question;
    task.textContent = lesson.task;
    term.textContent = lesson.term;
    transfer.textContent = lesson.transfer;

    const render = (state) => {
      if (document.activeElement !== before) before.value = state.before || '';
      if (document.activeElement !== revise) revise.value = state.revise || '';
      start.disabled = (state.before || '').trim().length < 2;
      start.textContent = state.started ? '更新判断' : '留下判断';
      progress.textContent = state.started ? `已记录 · 对照 ${state.evidence}/2` : '先留下判断，再操作';
      resultProgress.textContent = state.started
        ? `已经比较 ${state.evidence}/2 个状态`
        : '上面的判断留下后，这里才开始记录对照。';
      reveal.hidden = !state.ready;
      gate.hidden = state.ready;
      if (!state.started) gate.textContent = '先在上面留下一句判断。';
      else if (state.evidence < 2) gate.textContent = '再改变一次同一个控制量，比较两个状态。';
      else if (!state.reflected) gate.textContent = '把你看见的变化写成一句话，再看背后的关系。';
    };
    before.addEventListener('input', () => dispatch('set-before', before.value));
    revise.addEventListener('input', () => dispatch('set-revise', revise.value));
    start.addEventListener('click', () => dispatch('start'));
    return { render };
  }

  const removeStandalone = () => {
    if (!standalone) return;
    stateListeners.delete(standalone.ui.render);
    if (standalone.stage) {
      const parent = standalone.stage.parentNode;
      while (standalone.stage.firstChild) {
        const child = standalone.stage.firstChild;
        child.querySelectorAll?.('.learning-cycle-was-fixed').forEach((element) => element.classList.remove('learning-cycle-was-fixed'));
        child.classList?.remove('learning-cycle-was-fixed');
        parent.insertBefore(child, standalone.stage);
      }
      standalone.stage.remove();
    }
    if (standalone.questionOwned) standalone.question.remove();
    else {
      standalone.question.replaceChildren();
      standalone.question.classList.remove('learning-cycle-flow-mount', 'learning-cycle-flow-mount--question');
      delete standalone.question.dataset.learningCycleOwned;
    }
    if (standalone.resultOwned) standalone.result.remove();
    else {
      standalone.result.replaceChildren();
      standalone.result.classList.remove('learning-cycle-flow-mount', 'learning-cycle-flow-mount--result');
      delete standalone.result.dataset.learningCycleOwned;
    }
    standalone = null;
    document.documentElement.classList.remove('learning-cycle-standalone');
    scheduleResize();
  };
  const mountStandalone = () => {
    if (hosted || standalone) return;
    document.documentElement.classList.add('learning-cycle-standalone');
    const explicitQuestion = document.querySelector('[data-learning-cycle-mount]');
    const explicitResult = document.querySelector('[data-learning-result-mount]');
    const questionMount = explicitQuestion || document.createElement('div');
    const resultMount = explicitResult || document.createElement('div');
    let stage = null;
    if (frameLayout === 'studio' && !explicitQuestion && !explicitResult) {
      stage = document.createElement('div');
      stage.className = 'learning-cycle-standalone-stage';
      const originalChildren = [...document.body.children].filter((element) => element.tagName !== 'SCRIPT');
      document.body.insertBefore(questionMount, document.body.firstChild);
      questionMount.insertAdjacentElement('afterend', stage);
      stage.insertAdjacentElement('afterend', resultMount);
      originalChildren.forEach((element) => {
        [element, ...element.querySelectorAll('*')].forEach((candidate) => {
          if (getComputedStyle(candidate).position === 'fixed') candidate.classList.add('learning-cycle-was-fixed');
        });
        stage.appendChild(element);
      });
    } else if (!explicitQuestion || !explicitResult) {
      const main = document.querySelector('main');
      const scene = main || document.querySelector('[data-lab-scene],#scene-wrap,#scene,.stage,.scene,canvas,svg');
      if (!explicitQuestion) {
        if (scene && scene.parentNode) scene.parentNode.insertBefore(questionMount, scene);
        else document.body.insertBefore(questionMount, document.body.firstChild);
      }
      if (!explicitResult) {
        const anchor = main || scene;
        if (anchor && anchor.parentNode) anchor.parentNode.insertBefore(resultMount, anchor.nextSibling);
        else document.body.appendChild(resultMount);
      }
    }
    const ui = renderLearningUI(questionMount, resultMount, applyCommand);
    standalone = {
      question: questionMount,
      result: resultMount,
      questionOwned: !explicitQuestion,
      resultOwned: !explicitResult,
      stage,
      ui
    };
    stateListeners.add(ui.render);
    ui.render(statePayload());
    scheduleResize();
  };

  window.addEventListener('message', (event) => {
    if (!embedded || event.source !== window.parent) return;
    const message = event.data || {};
    if (message.source !== hostTag) return;
    if (message.type === 'request-init') {
      postToParent('init', { lesson, state: statePayload() });
      return;
    }
    if (message.type === 'mount') {
      hosted = true;
      removeStandalone();
      postToParent('init', { lesson, state: statePayload() });
      notifyState();
      return;
    }
    if (message.type === 'command') applyCommand(message.command, message.value);
  });

  document.addEventListener('change', (event) => {
    if (event.target.matches('input,select') && !event.target.closest('[data-learning-cycle-owned]')) {
      addEvidence(event.target);
    }
  }, true);
  document.addEventListener('click', (event) => {
    const control = event.target.closest('button,[role="button"]');
    if (control && !control.closest('[data-learning-cycle-owned]')) {
      queueMicrotask(() => addEvidence(control));
    }
  }, true);
  document.addEventListener('pointerup', (event) => {
    if (!started || event.target.closest('[data-learning-cycle-owned]')) return;
    const surface = event.target.closest('canvas,svg');
    if (!surface) return;
    const rect = surface.getBoundingClientRect();
    if (!rect.width || !rect.height) return;
    const key = `surface:${surface.id || surface.getAttribute('aria-label') || 'graphic'}`;
    const values = stateHistory.get(key) || new Set();
    values.add(`${Math.round(((event.clientX - rect.left) / rect.width) * 10)}:${Math.round(((event.clientY - rect.top) / rect.height) * 10)}`);
    stateHistory.set(key, values);
    persist();
    notifyState();
  }, true);

  const studioFiles = new Set([
    '03-reaction-bridge-3d.html',
    'arch-bridge-hybrid-fem.html',
    'bridge-shell-mitc4.html'
  ]);
  const frameLayout = document.documentElement.dataset.layout
    || document.body.dataset.layout
    || (studioFiles.has(file) ? 'studio' : 'flow');
  let resizeFrame = 0;
  function reportSize() {
    resizeFrame = 0;
    if (!embedded) return;
    const root = document.documentElement;
    const body = document.body;
    const height = Math.ceil(Math.max(
      root.scrollHeight,
      root.offsetHeight,
      body ? body.scrollHeight : 0,
      body ? body.offsetHeight : 0
    ));
    window.parent.postMessage({
      source: shellTag,
      type: 'resize',
      height,
      layout: frameLayout,
      id
    }, '*');
  }
  function scheduleResize() {
    if (resizeFrame) return;
    resizeFrame = requestAnimationFrame(reportSize);
  }
  if ('ResizeObserver' in window) {
    const observer = new ResizeObserver(scheduleResize);
    observer.observe(document.documentElement);
    if (document.body) observer.observe(document.body);
  }
  window.addEventListener('load', scheduleResize, { once: true });
  window.addEventListener('resize', scheduleResize);

  if (started) snapshotInitialStates();
  postToParent('init', { lesson, state: statePayload() });
  [120, 450, 1200].forEach((delay) => setTimeout(() => {
    if (!hosted) postToParent('init', { lesson, state: statePayload() });
  }, delay));
  setTimeout(() => {
    if (!hosted) mountStandalone();
  }, embedded ? 900 : 0);
  notifyState();
  scheduleResize();
})();
