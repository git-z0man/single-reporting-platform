/* Single Reporting Platform — Manufacturer's guide
   - Active-section highlighting for the sidebar nav (desktop)
   - Floating section bar (mobile): current location + prev/next + jump menu
   - Lightbox: click a screenshot to view it full size
   The FAQ "+" → "×" chevron rotation is handled purely in CSS. */

(function () {
  var SECTIONS = [
    { id: 'reg', num: '01', label: 'Registration' },
    { id: 'ew',  num: '02', label: 'Early Warning' },
    { id: 'n72', num: '03', label: '72 h Notification' },
    { id: 'fin', num: '04', label: 'Final Report' },
    { id: 'faq', num: '·', label: 'Questions & answers' }
  ];
  var indexOf = {};
  SECTIONS.forEach(function (s, i) { indexOf[s.id] = i; });

  // sidebar links
  var tocLinks = {};
  document.querySelectorAll('[data-toc]').forEach(function (a) {
    tocLinks[a.getAttribute('data-toc')] = a;
  });

  // floating bar
  var fb = document.querySelector('.floatbar');
  var fbCur = fb && fb.querySelector('.fb-cur');
  var fbNum = fb && fb.querySelector('.fb-num');
  var fbLabel = fb && fb.querySelector('.fb-label');
  var fbPrev = fb && fb.querySelector('.fb-prev');
  var fbNext = fb && fb.querySelector('.fb-next');
  var fbMenuLinks = fb ? fb.querySelectorAll('.fb-menu a') : [];

  var currentIndex = 0;

  function setActive(id) {
    if (!(id in indexOf)) return;
    currentIndex = indexOf[id];

    Object.keys(tocLinks).forEach(function (key) {
      tocLinks[key].classList.toggle('active', key === id);
    });

    if (fb) {
      var s = SECTIONS[currentIndex];
      fbNum.textContent = s.num;
      fbLabel.textContent = s.label;
      fbPrev.disabled = currentIndex === 0;
      fbNext.disabled = currentIndex === SECTIONS.length - 1;
      fbMenuLinks.forEach(function (a) {
        a.classList.toggle('active', a.getAttribute('data-fb') === id);
      });
    }
  }

  function goTo(idx) {
    if (idx < 0 || idx >= SECTIONS.length) return;
    var el = document.getElementById(SECTIONS[idx].id);
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  // ---- active-section observer ----
  if ('IntersectionObserver' in window) {
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) setActive(e.target.id); });
    }, { rootMargin: '-10% 0px -80% 0px', threshold: 0 });
    SECTIONS.forEach(function (s) {
      var el = document.getElementById(s.id);
      if (el) obs.observe(el);
    });
  }

  // ---- floating bar interactions ----
  if (fb) {
    function closeMenu() { fb.classList.remove('menu-open'); fbCur.setAttribute('aria-expanded', 'false'); }

    fbPrev.addEventListener('click', function () { goTo(currentIndex - 1); closeMenu(); });
    fbNext.addEventListener('click', function () { goTo(currentIndex + 1); closeMenu(); });

    fbCur.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = fb.classList.toggle('menu-open');
      fbCur.setAttribute('aria-expanded', open ? 'true' : 'false');
    });

    fbMenuLinks.forEach(function (a) {
      a.addEventListener('click', closeMenu);
    });

    document.addEventListener('click', function (e) {
      if (fb.classList.contains('menu-open') && !fb.contains(e.target)) closeMenu();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeMenu();
    });
  }
})();

/* Lightbox — click a screenshot to view it full size; ‹ / › or arrow keys
   step through all screenshots in document order. */
(function () {
  var lb = document.getElementById('lb');
  if (!lb) return;
  var img = lb.querySelector('.lb-img');
  var cap = lb.querySelector('.lb-cap');
  var prevBtn = lb.querySelector('.lb-prev');
  var nextBtn = lb.querySelector('.lb-next');

  // ordered list of viewable screenshots (skip any with a missing image)
  var shots = Array.prototype.filter.call(
    document.querySelectorAll('img.shot'),
    function (s) { var f = s.closest('figure'); return !(f && f.classList.contains('missing')); }
  );
  var idx = -1;

  function show(i) {
    idx = (i + shots.length) % shots.length;
    var shot = shots[idx];
    var fig = shot.closest('figure');
    var caption = fig ? fig.querySelector('figcaption') : null;
    img.src = shot.dataset.full || shot.currentSrc || shot.src;
    cap.textContent = caption ? caption.textContent : '';
  }
  function openAt(shot) {
    show(shots.indexOf(shot));
    lb.hidden = false;
    lb.classList.add('open');
  }
  function close() {
    lb.classList.remove('open');
    lb.hidden = true;
    img.src = '';
    idx = -1;
  }
  var isOpen = function () { return lb.classList.contains('open'); };

  shots.forEach(function (shot) {
    shot.addEventListener('click', function () { openAt(shot); });
  });

  // nav buttons must not bubble to the backdrop (which closes)
  prevBtn.addEventListener('click', function (e) { e.stopPropagation(); show(idx - 1); });
  nextBtn.addEventListener('click', function (e) { e.stopPropagation(); show(idx + 1); });
  img.addEventListener('click', function (e) { e.stopPropagation(); });

  lb.addEventListener('click', close);
  document.addEventListener('keydown', function (e) {
    if (!isOpen()) return;
    if (e.key === 'Escape') close();
    else if (e.key === 'ArrowLeft') show(idx - 1);
    else if (e.key === 'ArrowRight') show(idx + 1);
  });
})();

// ---- theme toggle ----------------------------------------------------
(function () {
  var btn = document.querySelector('.theme-toggle');
  if (!btn) return;
  var root = document.documentElement;
  var mql = window.matchMedia('(prefers-color-scheme: dark)');

  function current() {
    var explicit = root.getAttribute('data-theme');
    if (explicit) return explicit;
    return mql.matches ? 'dark' : 'light';
  }
  function apply(theme) {
    root.setAttribute('data-theme', theme);
    btn.setAttribute('aria-pressed', String(theme === 'dark'));
    try { localStorage.setItem('theme', theme); } catch (e) {}
  }

  btn.setAttribute('aria-pressed', String(current() === 'dark'));
  btn.addEventListener('click', function () {
    apply(current() === 'dark' ? 'light' : 'dark');
  });
})();
