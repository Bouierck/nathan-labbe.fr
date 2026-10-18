/* nathan-labbe.fr — comportements. Le site reste lisible et utilisable sans JS. */
(() => {
  const root = document.documentElement;
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* 1. Image absente : on essaie les autres extensions listées dans data-ext (ex. "webp jpg"),
        puis on masque proprement l'emplacement au lieu d'afficher une icône cassée. */
  document.querySelectorAll('[data-img] img').forEach((img) => {
    const base = img.getAttribute('src').replace(/\.[a-z0-9]+$/i, '');
    const others = (img.dataset.ext || '').split(/\s+/).filter(Boolean).map((ext) => `${base}.${ext}`);
    const fail = () => {
      const next = others.shift();
      if (next) img.src = next;
      else img.closest('[data-img]').classList.add('img-missing');
    };
    img.addEventListener('error', fail);
    if (img.complete && img.naturalWidth === 0) fail();
  });

  /* 2. Menu mobile (la même <nav> sert de règle sur grand écran). */
  const nav = document.getElementById('sections');
  const btn = document.querySelector('.topbar-btn');
  if (nav && btn) {
    root.classList.add('has-menu');
    const setOpen = (open) => {
      btn.setAttribute('aria-expanded', String(open));
      btn.textContent = open ? 'Fermer' : 'Menu';
      nav.classList.toggle('is-open', open);
    };
    btn.addEventListener('click', () => setOpen(btn.getAttribute('aria-expanded') !== 'true'));
    nav.addEventListener('click', (e) => {
      if (e.target.closest('a')) setOpen(false);
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) {
        setOpen(false);
        btn.focus();
      }
    });
    document.addEventListener('click', (e) => {
      if (nav.classList.contains('is-open') && !nav.contains(e.target) && !btn.contains(e.target)) setOpen(false);
    });
  }

  /* 3. Section active : repère orange sur la règle. */
  if (nav && 'IntersectionObserver' in window) {
    const links = [...nav.querySelectorAll('a[href^="#"]')];
    const linkFor = new Map(links.map((a) => [a.getAttribute('href').slice(1), a]));
    const setActive = (id) => {
      const target = linkFor.get(id);
      if (!target || target.getAttribute('aria-current') === 'true') return;
      links.forEach((a) => a.removeAttribute('aria-current'));
      target.setAttribute('aria-current', 'true');
    };
    // En bas de page, la dernière section (courte) ne passe jamais au milieu de l'écran.
    const last = links[links.length - 1].getAttribute('href').slice(1);
    const atBottom = () => window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 4;
    const io = new IntersectionObserver((entries) => {
      if (atBottom()) return setActive(last);
      entries.forEach((entry) => {
        if (entry.isIntersecting) setActive(entry.target.id);
      });
    }, { rootMargin: '-40% 0px -55% 0px' });
    linkFor.forEach((_, id) => {
      const section = document.getElementById(id);
      if (section) io.observe(section);
    });
    window.addEventListener('scroll', () => {
      if (atBottom()) setActive(last);
    }, { passive: true });
  }

  /* 4. Parcours : les barres se tracent quand le diagramme arrive à l'écran. */
  const gantt = document.querySelector('.gantt');
  if (gantt && !reduceMotion && 'IntersectionObserver' in window) {
    gantt.classList.add('will-draw');
    const draw = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) {
        gantt.classList.add('is-drawn');
        draw.disconnect();
      }
    }, { threshold: 0.2 });
    draw.observe(gantt);
  }
})();
