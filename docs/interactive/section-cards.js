(() => {
  'use strict';

  /*
   * The reviewed source data stays rich.  The reading UI deliberately reveals
   * it in layers: one retrieval prompt, one short answer, then optional detail.
   */
  const DATA = window.BRIDGE_SECTION_CARDS || {};
  const chapter = (location.pathname.split('/').pop() || '').replace(/\.html$/i, '');
  const sections = DATA[chapter];
  if (!sections) return;

  const normalize = (value) => String(value || '')
    .replace(/\u00a0/g, ' ')
    .replace(/[“”]/g, '"')
    .replace(/[‘’]/g, "'")
    .replace(/\s+/g, ' ')
    .replace(/^#+\s*/, '')
    .trim();

  const sectionMap = new Map(
    Object.entries(sections).map(([heading, cards]) => [normalize(heading), cards])
  );

  const text = (tag, className, value) => {
    const node = document.createElement(tag);
    if (className) node.className = className;
    node.textContent = value;
    return node;
  };

  const makeButton = (className, label, ariaLabel = '') => {
    const button = text('button', className, label);
    button.type = 'button';
    if (ariaLabel) button.setAttribute('aria-label', ariaLabel);
    return button;
  };

  const characters = (value) => Array.from(String(value || ''));

  const trimText = (value, max = 90, minBreak = 35) => {
    const clean = normalize(value);
    const chars = characters(clean);
    if (chars.length <= max) return clean;

    const slice = chars.slice(0, max);
    const preferred = new Set(['。', '！', '？', '；']);
    let cut = -1;
    for (let index = slice.length - 1; index >= minBreak; index -= 1) {
      if (preferred.has(slice[index])) {
        cut = index + 1;
        break;
      }
    }
    if (cut > 0) return slice.slice(0, cut).join('');

    for (let index = slice.length - 2; index >= minBreak; index -= 1) {
      if (slice[index] === '，') {
        cut = index + 1;
        break;
      }
    }
    return `${slice.slice(0, cut > 0 ? cut : max - 1).join('').replace(/[，；\s]+$/, '')}…`;
  };

  const shortAnswer = (card) => {
    const idea = normalize(card.idea);
    const mechanism = normalize(card.mechanism);
    if (characters(idea).length >= 35) return trimText(idea);
    return trimText([idea, mechanism].filter(Boolean).join(' '));
  };

  const splitToolHelp = (value) => {
    const raw = normalize(value);
    const separators = [raw.indexOf('；'), raw.indexOf(';')].filter((index) => index >= 0);
    const cut = separators.length ? Math.min(...separators) : -1;
    if (cut < 0) return { tool: raw, boundary: '' };
    return {
      tool: raw.slice(0, cut).trim().replace(/[。.]$/, ''),
      boundary: raw.slice(cut + 1).trim().replace(/[。.]$/, '')
    };
  };

  const addDetail = (host, label, value) => {
    if (!value || (Array.isArray(value) && !value.length)) return;
    const row = document.createElement('div');
    row.className = 'section-flashcard__detail-row';
    row.append(
      text('dt', '', label),
      text('dd', '', Array.isArray(value) ? value.join('；') : value)
    );
    host.appendChild(row);
  };

  const storageKey = (heading) =>
    `bridge-section-deck:v1:${chapter}:${normalize(heading)}`;

  const readState = (heading, cardCount) => {
    const fallback = {
      mode: 'core',
      current: 0,
      ratings: {},
      round: null,
      finished: false
    };
    try {
      const saved = JSON.parse(localStorage.getItem(storageKey(heading)) || 'null');
      if (!saved || typeof saved !== 'object') return fallback;
      const ratings = {};
      Object.entries(saved.ratings || {}).forEach(([index, rating]) => {
        const number = Number(index);
        if (number >= 0 && number < cardCount && ['missed', 'clear'].includes(rating)) {
          ratings[number] = rating;
        }
      });
      const roundIndices = Array.isArray(saved.round?.indices)
        ? [...new Set(saved.round.indices.map(Number))].filter((index) => index >= 0 && index < cardCount)
        : [];
      return {
        mode: saved.mode === 'deep' ? 'deep' : 'core',
        current: Math.min(Math.max(Number(saved.current) || 0, 0), cardCount - 1),
        ratings,
        round: roundIndices.length ? { kind: saved.round.kind || 'all', indices: roundIndices } : null,
        finished: Boolean(saved.finished)
      };
    } catch (_) {
      return fallback;
    }
  };

  const writeState = (heading, state) => {
    try { localStorage.setItem(storageKey(heading), JSON.stringify(state)); } catch (_) {}
  };

  const buildDeck = (heading, cards) => {
    const group = document.createElement('section');
    group.className = 'section-flashcards';
    group.setAttribute('aria-label', `${heading}的闪卡练习`);

    const toolbar = document.createElement('div');
    toolbar.className = 'section-flashcards__toolbar';

    const modeGroup = document.createElement('div');
    modeGroup.className = 'section-flashcards__modes';
    modeGroup.setAttribute('role', 'group');
    modeGroup.setAttribute('aria-label', '选择练习范围');
    const coreButton = makeButton('section-flashcards__mode', '先看一张', '只练习第一张卡');
    const deepButton = makeButton('section-flashcards__mode', `本节全练·${cards.length}`, `练习本小节全部 ${cards.length} 张卡`);
    modeGroup.append(coreButton, deepButton);
    if (cards.length === 1) deepButton.hidden = true;

    const deviceNote = text('span', 'section-flashcards__device-note', '进度保存在本设备');
    toolbar.append(modeGroup, deviceNote);

    const stage = document.createElement('div');
    stage.className = 'section-flashcards__stage';
    stage.setAttribute('aria-live', 'polite');

    const progress = document.createElement('div');
    progress.className = 'section-flashcards__progress';
    progress.setAttribute('role', 'progressbar');
    const progressBar = document.createElement('span');
    progress.appendChild(progressBar);

    group.append(toolbar, stage, progress);

    let state = readState(heading, cards.length);
    let flipped = false;

    const baseIndices = () => state.mode === 'deep'
      ? cards.map((_, index) => index)
      : [0];

    const queue = () => {
      const allowed = new Set(baseIndices());
      const savedRound = Array.isArray(state.round?.indices)
        ? state.round.indices.filter((index) => allowed.has(index))
        : [];
      return savedRound.length ? savedRound : baseIndices();
    };

    const ensureCurrent = () => {
      const indices = queue();
      if (!indices.includes(state.current)) state.current = indices[0];
      return indices;
    };

    const setMode = (mode) => {
      if (mode === 'deep' && cards.length === 1) return;
      state.mode = mode;
      state.current = 0;
      state.round = null;
      state.finished = false;
      flipped = false;
      writeState(heading, state);
      render();
    };

    coreButton.addEventListener('click', () => setMode('core'));
    deepButton.addEventListener('click', () => setMode('deep'));

    const renderMode = () => {
      coreButton.classList.toggle('is-active', state.mode === 'core');
      deepButton.classList.toggle('is-active', state.mode === 'deep');
      coreButton.setAttribute('aria-pressed', String(state.mode === 'core'));
      deepButton.setAttribute('aria-pressed', String(state.mode === 'deep'));
    };

    const move = (delta) => {
      const indices = ensureCurrent();
      const position = indices.indexOf(state.current);
      const next = position + delta;
      if (next < 0 || next >= indices.length) return;
      state.current = indices[next];
      state.finished = false;
      flipped = false;
      writeState(heading, state);
      render();
    };

    const rate = (rating) => {
      state.ratings[state.current] = rating;
      const indices = ensureCurrent();
      const allRated = indices.every((index) => Boolean(state.ratings[index]));
      if (allRated) state.finished = true;
      writeState(heading, state);
      render();
    };

    const restart = (kind) => {
      const base = baseIndices();
      const indices = kind === 'missed'
        ? base.filter((index) => state.ratings[index] === 'missed')
        : base;
      if (!indices.length) return;
      indices.forEach((index) => { delete state.ratings[index]; });
      state.round = { kind, indices };
      state.current = indices[0];
      state.finished = false;
      flipped = false;
      writeState(heading, state);
      render();
    };

    const buildExplanation = (card) => {
      const why = document.createElement('details');
      why.className = 'section-flashcard__why';
      const summary = text('summary', '', '为什么会这样？');
      const list = document.createElement('dl');
      const toolHelp = splitToolHelp(card.aiHelp);
      addDetail(list, '怎么发生的', card.mechanism);
      addDetail(list, '什么时候不灵', toolHelp.boundary);
      addDetail(list, '还能连到哪里', card.connections);
      why.append(summary, list);
      return why;
    };

    const buildCard = (indices) => {
      const cardIndex = state.current;
      const card = cards[cardIndex];
      const position = indices.indexOf(cardIndex);
      const article = document.createElement('article');
      article.className = 'section-flashcard';
      article.dataset.side = flipped ? 'back' : 'front';

      const meta = document.createElement('div');
      meta.className = 'section-flashcard__meta';
      meta.append(
        text('span', 'section-flashcard__principle', card.concept || card.theme || '这一节'),
        text('span', 'section-flashcard__count', `${position + 1} / ${indices.length}`)
      );

      const front = document.createElement('div');
      front.className = 'section-flashcard__face section-flashcard__front';
      front.hidden = flipped;
      const question = text('p', 'section-flashcard__question', card.question);
      const reveal = makeButton('section-flashcard__reveal', '看答案');
      reveal.addEventListener('click', () => {
        flipped = true;
        render();
        stage.querySelector('.section-flashcard__rating')?.focus();
      });
      front.append(question, reveal);

      const back = document.createElement('div');
      back.className = 'section-flashcard__face section-flashcard__back';
      back.hidden = !flipped;
      back.append(
        text('p', 'section-flashcard__short-answer', shortAnswer(card)),
        buildExplanation(card)
      );

      const ratings = document.createElement('div');
      ratings.className = 'section-flashcard__ratings';
      ratings.setAttribute('role', 'group');
      ratings.setAttribute('aria-label', '这张卡的掌握情况');
      const missed = makeButton('section-flashcard__rating section-flashcard__rating--missed', '还没抓住');
      const clear = makeButton('section-flashcard__rating section-flashcard__rating--clear', '我能说清楚');
      const currentRating = state.ratings[cardIndex];
      missed.classList.toggle('is-selected', currentRating === 'missed');
      clear.classList.toggle('is-selected', currentRating === 'clear');
      missed.setAttribute('aria-pressed', String(currentRating === 'missed'));
      clear.setAttribute('aria-pressed', String(currentRating === 'clear'));
      missed.addEventListener('click', () => rate('missed'));
      clear.addEventListener('click', () => rate('clear'));
      ratings.append(missed, clear);
      back.appendChild(ratings);

      const navigation = document.createElement('nav');
      navigation.className = 'section-flashcard__navigation';
      navigation.setAttribute('aria-label', '闪卡导航');
      const previous = makeButton('section-flashcard__nav', '←', '上一张卡');
      const next = makeButton('section-flashcard__nav', '→', '下一张卡');
      previous.disabled = position === 0;
      next.disabled = position === indices.length - 1;
      previous.addEventListener('click', () => move(-1));
      next.addEventListener('click', () => move(1));
      navigation.append(previous, next);

      article.append(meta, front, back, navigation);
      return article;
    };

    const buildFinish = (indices) => {
      const clearCount = indices.filter((index) => state.ratings[index] === 'clear').length;
      const missedIndices = indices.filter((index) => state.ratings[index] === 'missed');
      const finish = document.createElement('div');
      finish.className = 'section-flashcards__finish';
      finish.append(
        text('p', 'section-flashcards__finish-title', '这一轮结束了'),
        text('p', 'section-flashcards__finish-counts', `能说清楚 ${clearCount} · 还没抓住 ${missedIndices.length}`)
      );
      const actions = document.createElement('div');
      actions.className = 'section-flashcards__finish-actions';
      if (missedIndices.length) {
        const retryMissed = makeButton('section-flashcards__retry section-flashcards__retry--primary', '只重练没抓住');
        retryMissed.addEventListener('click', () => restart('missed'));
        actions.appendChild(retryMissed);
      }
      const retryAll = makeButton('section-flashcards__retry', '全部再来');
      retryAll.addEventListener('click', () => restart('all'));
      actions.appendChild(retryAll);
      finish.appendChild(actions);
      return finish;
    };

    const render = () => {
      const indices = ensureCurrent();
      renderMode();
      stage.replaceChildren(state.finished ? buildFinish(indices) : buildCard(indices));
      const rated = indices.filter((index) => Boolean(state.ratings[index])).length;
      const progressValue = state.finished ? 100 : (rated / indices.length) * 100;
      progressBar.style.width = `${progressValue}%`;
      progress.setAttribute('aria-valuemin', '0');
      progress.setAttribute('aria-valuemax', String(indices.length));
      progress.setAttribute('aria-valuenow', String(state.finished ? indices.length : rated));
      progress.setAttribute('aria-label', `已完成 ${rated} / ${indices.length} 张`);
      writeState(heading, state);
    };

    group.addEventListener('keydown', (event) => {
      if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
      if (event.key === 'ArrowLeft') {
        event.preventDefault();
        move(-1);
      }
      if (event.key === 'ArrowRight') {
        event.preventDefault();
        move(1);
      }
    });

    render();
    return group;
  };

  let inserted = 0;
  const headings = [...document.querySelectorAll('main h2, main.content h2')];
  headings.forEach((heading) => {
    const name = normalize(heading.textContent);
    const cards = sectionMap.get(name);
    if (!Array.isArray(cards) || !cards.length) return;
    heading.insertAdjacentElement('afterend', buildDeck(name, cards));
    inserted += 1;
  });

  if (inserted !== sectionMap.size) {
    const visibleHeadings = new Set(headings.map((heading) => normalize(heading.textContent)));
    const missing = [...sectionMap.keys()].filter((name) => !visibleHeadings.has(name));
    if (missing.length) console.warn('[section-cards] headings not found:', missing);
  }
})();
