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
    { id: 'roles', num: '·', label: 'Accounts & roles' },
    { id: 'fields', num: '·', label: 'Every field, explained' },
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

/* ---- field reference: jump from a phase table to the full entry ----------
   The phase tables link a field number to its entry in "Every field,
   explained". The entries are <details>, so a plain anchor would scroll to a
   closed box; open it first, and switch to the cards view if the table view
   is showing. */
(function () {
  function reveal(hash) {
    if (!hash || hash.charAt(0) !== '#') return;
    var el;
    try { el = document.querySelector(hash); } catch (e) { return; }
    if (!el || el.tagName !== 'DETAILS') return;
    var sw = document.querySelector('.viewswitch .vsbtn[data-view="cards"]');
    if (sw && sw.getAttribute('aria-pressed') === 'false') sw.click();
    el.open = true;
    el.scrollIntoView({ behavior: 'smooth', block: 'center' });
    el.classList.add('flash');
    setTimeout(function () { el.classList.remove('flash'); }, 1400);
  }

  document.querySelectorAll('a.fieldref').forEach(function (a) {
    a.addEventListener('click', function (e) {
      e.preventDefault();
      var hash = a.getAttribute('href');
      if (history.replaceState) history.replaceState(null, '', hash);
      reveal(hash);
    });
  });

  window.addEventListener('hashchange', function () { reveal(location.hash); });
  if (location.hash) reveal(location.hash);
})();

/* ---- field reference: cards <-> full table ------------------------------
   The table is generated from the cards, so there is one copy of the text and
   the two views cannot drift apart. */
(function () {
  var sw = document.querySelector('.viewswitch');
  var cards = document.getElementById('fieldcards');
  var table = document.getElementById('fieldtable');
  if (!sw || !cards || !table) return;

  var built = false;

  // each block of a field card is tagged with data-k; read it by key rather
  // than by matching a label's text, which broke the moment labels moved out
  // of the paragraph they introduced.
  function part(body, key) {
    var el = body.querySelector('[data-k="' + key + '"]');
    return el ? el.innerHTML.trim() : '';
  }

  var STAGES = ['EW', '72\u2009h', 'FR'];
  function stageCell(chips) {
    if (!chips) return '';
    var out = '';
    Array.prototype.forEach.call(chips.querySelectorAll('.chip'), function (c, i) {
      out += '<span class="ft-stage"><b>' + (STAGES[i] || '') + '</b>' + c.outerHTML + '</span>';
    });
    return out;
  }

  function build() {
    var html = '';
    var groups = cards.querySelectorAll('.faq-wrap');
    groups.forEach(function (wrap) {
      // the group's own heading and subtitle sit just before the wrapper
      var label = '', sub = '';
      var p = wrap.previousElementSibling;
      while (p) {
        if (p.classList.contains('fieldgroup-sub')) sub = p.textContent;
        else if (p.classList.contains('seclabel')) {
          var t = p.querySelector('.seclabel-text');
          label = t ? t.textContent : '';
          break;
        }
        p = p.previousElementSibling;
      }

      html += '<div class="seclabel"><span class="seclabel-bar"></span><span class="seclabel-text">' +
              label + '</span></div>';
      if (sub) html += '<p class="fieldgroup-sub">' + sub + '</p>';
      html += '<div class="table-wrap"><table class="data fieldtable">' +
              '<colgroup><col class="ft-num"><col class="ft-name"><col class="ft-mean">' +
              '<col class="ft-how"><col class="ft-st"></colgroup>' +
              '<thead><tr><th>#</th><th>Field</th><th>What it means</th>' +
              '<th>How ENISA says to complete it</th>' +
              '<th>EW · 72&nbsp;h · FR</th></tr></thead><tbody>';

      wrap.querySelectorAll('details.field').forEach(function (d) {
        var num = d.querySelector('.faq-num').textContent;
        var name = d.querySelector('.faq-qwrap span:last-child').textContent;
        var body = d.querySelector('.faq-body');
        var src = body.querySelector('.field-src');
        var chips = d.querySelector('.field-chips');
        var ex = part(body, 'ex');
        var fmt = part(body, 'fmt');
        var foot = body.querySelector('.field-foot');

        html += '<tr id="ft-' + num + '">' +
                '<td class="ft-num"><span class="faq-num">' + num + '</span></td>' +
                '<td class="ft-name"><strong>' + name + '</strong>' +
                (src ? '<span class="ft-src">' + src.innerHTML + '</span>' : '') + '</td>' +
                '<td>' + part(body, 'means') + '</td>' +
                '<td>' + part(body, 'how') +
                (ex ? '<span class="ft-sub"><b>Example</b> ' + ex + '</span>' : '') +
                (fmt ? '<span class="ft-sub"><b>Format</b> ' + fmt + '</span>' : '') +
                (foot ? '<span class="ft-sub note">' + foot.innerHTML + '</span>' : '') +
                '</td>' +
                '<td class="ft-st">' + stageCell(chips) + '</td>' +
                '</tr>';
      });
      html += '</tbody></table></div>';
    });
    table.innerHTML = html;
    built = true;
  }

  sw.querySelectorAll('.vsbtn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var wantTable = btn.dataset.view === 'table';
      if (wantTable && !built) build();
      cards.hidden = wantTable;
      table.hidden = !wantTable;
      sw.querySelectorAll('.vsbtn').forEach(function (b) {
        b.setAttribute('aria-pressed', String((b.dataset.view === 'table') === wantTable));
      });
    });
  });
})();

/* ---- field cards: note markers and open-all ------------------------------
   The header marker says which kinds of note a card holds, so a reader can
   see it without opening all 38. It is derived from the card's own content,
   never written into the markup: add or remove a note and the marker follows
   by itself. */
(function () {
  var cards = document.querySelectorAll('#fieldcards details.field');
  if (!cards.length) return;

  cards.forEach(function (d) {
    var marks = [];
    if (d.querySelector('.ownnote')) {
      marks.push('<span class="notemark own" title="Carries a note from practice">' +
                 '<span class="notemark-ic" aria-hidden="true">✱</span>From practice</span>');
    }
    if (d.querySelector('.faq-amend')) {
      marks.push('<span class="notemark src" title="Carries a remark on ENISA’s own text">' +
                 '<span class="notemark-ic" aria-hidden="true">⚑</span>Source note</span>');
    }
    if (!marks.length) return;
    var wrap = document.createElement('span');
    wrap.className = 'notemarks';
    wrap.innerHTML = marks.join('');
    // as a sibling of the title block, not inside it: nested in .faq-qwrap the
    // marker competes with the field name for width and shreds it on a phone
    var sum = d.querySelector('summary');
    sum.insertBefore(wrap, sum.querySelector('.field-chips'));
  });

  // "Open all" / "Close all", one per field group
  document.querySelectorAll('#fieldcards .openall').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var label = btn.closest('.seclabel');
      var wrap = label && label.nextElementSibling;
      while (wrap && !wrap.classList.contains('faq-wrap')) wrap = wrap.nextElementSibling;
      if (!wrap) return;
      var open = btn.dataset.open !== 'true';
      wrap.querySelectorAll('details.field').forEach(function (d) { d.open = open; });
      btn.dataset.open = String(open);
      btn.textContent = open ? 'Close all' : 'Open all';
    });
  });
})();
