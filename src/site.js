// Recipe scaling
(function () {
  const meta = document.querySelector('.recipe-meta[data-base-servings]');
  if (!meta) return;

  const base = parseFloat(meta.dataset.baseServings);
  if (!base || isNaN(base)) return;

  let current = base;
  const counter = meta.querySelector('.stepper-count');
  const minusBtn = meta.querySelector('.stepper-minus');
  const plusBtn = meta.querySelector('.stepper-plus');
  const items = document.querySelectorAll('li[data-ingredient]');

  const FRAC_TO_DEC = {
    '1/2': 0.5, '1/3': 1 / 3, '2/3': 2 / 3, '1/4': 0.25, '3/4': 0.75,
    '1/5': 0.2, '2/5': 0.4, '3/5': 0.6, '4/5': 0.8,
    '1/6': 1 / 6, '5/6': 5 / 6, '1/8': 0.125, '3/8': 0.375,
    '5/8': 0.625, '7/8': 0.875,
    '½': 0.5, '⅓': 1 / 3, '⅔': 2 / 3, '¼': 0.25, '¾': 0.75,
    '⅕': 0.2, '⅖': 0.4, '⅗': 0.6, '⅘': 0.8,
    '⅙': 1 / 6, '⅚': 5 / 6, '⅛': 0.125, '⅜': 0.375,
    '⅝': 0.625, '⅞': 0.875
  };

  function parseAmount(str) {
    str = str.trim();
    if (FRAC_TO_DEC[str] !== undefined) return FRAC_TO_DEC[str];

    const plain = parseFloat(str.replace(',', '.'));
    if (!isNaN(plain)) {
      const lastChar = str[str.length - 1];
      if (FRAC_TO_DEC[lastChar] !== undefined) return Math.floor(plain) + FRAC_TO_DEC[lastChar];
      return plain;
    }

    return null;
  }

  function fmt(n) {
    const rounded = Math.round(n * 10) / 10;
    return Number.isInteger(rounded) ? String(rounded) : rounded.toFixed(1).replace('.', ',');
  }

  const TOKEN_RE = /(\d+[.,]?\d*|\d*[½⅓⅔¼¾⅕⅖⅗⅘⅙⅚⅛⅜⅝⅞]|[½⅓⅔¼¾⅕⅖⅗⅘⅙⅚⅛⅜⅝⅞])/;

  function scaleText(original, ratio) {
    if (/\d\s*%/.test(original)) return original;

    return original.replace(TOKEN_RE, (match) => {
      const val = parseAmount(match);
      if (val === null) return match;
      return fmt(val * ratio);
    });
  }

  function render() {
    const ratio = current / base;
    counter.textContent = current;
    minusBtn.disabled = current <= 1;

    items.forEach((li) => {
      const orig = li.dataset.ingredient;
      li.textContent = ratio === 1 ? orig : scaleText(orig, ratio);
    });
  }

  minusBtn.addEventListener('click', () => {
    if (current > 1) {
      current--;
      render();
    }
  });

  plusBtn.addEventListener('click', () => {
    current++;
    render();
  });

  render();
})();

// Photo carousel
(function () {
  document.querySelectorAll('.photo-carousel').forEach((carousel) => {
    const items = carousel.querySelectorAll('.carousel-item');
    if (items.length < 2) return;

    let track = carousel.querySelector('.carousel-track');
    if (!track) {
      track = document.createElement('div');
      track.className = 'carousel-track';
      items.forEach((item) => track.appendChild(item));
      carousel.insertBefore(track, carousel.firstChild);
    }

    let current = 0;
    const counter = carousel.querySelector('.carousel-counter');
    const nextBtn = carousel.querySelector('.next');
    const prevBtn = carousel.querySelector('.prev');

    const show = (index) => {
      current = (index + items.length) % items.length;
      const peekCurrent = parseFloat(getComputedStyle(carousel).getPropertyValue('--peek-current')) || 80;
      track.style.transform = 'translateX(-' + (current * peekCurrent) + '%)';
      items.forEach((el, itemIndex) => el.classList.toggle('is-active', itemIndex === current));
      if (counter) counter.textContent = (current + 1) + ' / ' + items.length;
    };

    show(0);

    if (prevBtn) prevBtn.addEventListener('click', () => show(current - 1));
    if (nextBtn) nextBtn.addEventListener('click', () => show(current + 1));

    let touchStartX = 0;
    carousel.addEventListener('touchstart', (e) => {
      touchStartX = e.touches[0].clientX;
    }, { passive: true });

    carousel.addEventListener('touchend', (e) => {
      const dx = e.changedTouches[0].clientX - touchStartX;
      if (Math.abs(dx) > 40) show(dx < 0 ? current + 1 : current - 1);
    }, { passive: true });
  });
})();

// Discover grid: shuffle, filter and incremental reveal
(function () {
  const grid = document.getElementById('ontdek-grid');
  if (!grid) return;

  const cards = Array.from(grid.querySelectorAll('.toc-card'));
  const revealBtn = document.getElementById('ontdek-load-more');

  for (let i = cards.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    const tmp = cards[i];
    cards[i] = cards[j];
    cards[j] = tmp;
  }
  cards.forEach((card) => grid.appendChild(card));

  const activeFilter = { value: 'all' };

  const updateVisibility = () => {
    let visibleCount = 0;
    grid.querySelectorAll('.toc-card').forEach((card) => {
      const inFilter = activeFilter.value === 'all' || card.dataset.category === activeFilter.value;
      const discovered = card.classList.contains('is-discovered');
      const show = inFilter && discovered;
      card.style.display = show ? '' : 'none';
      if (show) visibleCount++;
    });

    if (!revealBtn) return;

    const remaining = cards.some((card) => {
      const inFilter = activeFilter.value === 'all' || card.dataset.category === activeFilter.value;
      return inFilter && !card.classList.contains('is-discovered');
    });

    revealBtn.style.display = remaining ? '' : 'none';
    revealBtn.setAttribute('aria-hidden', remaining ? 'false' : 'true');
  };

  const revealMore = () => {
    const batchSize = 48;
    let revealed = 0;
    for (const card of cards) {
      const inFilter = activeFilter.value === 'all' || card.dataset.category === activeFilter.value;
      if (inFilter && !card.classList.contains('is-discovered')) {
        card.classList.add('is-discovered');
        revealed++;
        if (revealed >= batchSize) break;
      }
    }
    updateVisibility();
  };

  const resetDiscoveryForFilter = () => {
    cards.forEach((card) => {
      const inFilter = activeFilter.value === 'all' || card.dataset.category === activeFilter.value;
      if (!inFilter) card.classList.remove('is-discovered');
    });
    revealMore();
  };

  document.querySelectorAll('.filter-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.filter-btn').forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');
      activeFilter.value = btn.dataset.cat;
      resetDiscoveryForFilter();
    });
  });

  if (revealBtn) revealBtn.addEventListener('click', revealMore);

  revealMore();
})();

// Netlify identity redirect
(function () {
  if (!window.netlifyIdentity) return;

  window.netlifyIdentity.on('init', (user) => {
    if (!user) {
      window.netlifyIdentity.on('login', () => {
        document.location.href = '/admin/';
      });
    }
  });
})();
