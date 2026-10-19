class ImgPopUp {
  constructor(targets = 'img', { nav = true } = {}) {
    this.images = typeof targets === 'string'
      ? Array.from(document.querySelectorAll(targets))
      : Array.from(targets);

    this.nav = nav;
    this.index = -1;

    // Shared lightbox for homepage images and album links.
    this.root = document.createElement('div');
    this.root.className = 'imgpop';
    this.root.hidden = true;
    this.root.setAttribute('role', 'dialog');
    this.root.setAttribute('aria-modal', 'true');
    this.root.setAttribute('aria-label', 'Photo viewer');

    const navHtml = this.nav
      ? `<button class="imgpop__btn imgpop__btn--prev" aria-label="Prev"></button>
         <button class="imgpop__btn imgpop__btn--next" aria-label="Next"></button>`
      : ``;

    this.root.innerHTML = `
      <img class="imgpop__img" alt="">
      <button type="button" class="imgpop__close" aria-label="Close photo viewer">&times;</button>
      <p class="imgpop__counter" aria-live="polite"></p>
      ${navHtml}
    `;
    document.body.appendChild(this.root);

    this.img  = this.root.querySelector('.imgpop__img');
    this.btnPrev = this.root.querySelector('.imgpop__btn--prev');
    this.btnNext = this.root.querySelector('.imgpop__btn--next');
    this.btnClose = this.root.querySelector('.imgpop__close');
    this.counter = this.root.querySelector('.imgpop__counter');
    this.btnClose.addEventListener('click', () => this.close());
    [this.btnPrev, this.btnNext].forEach(button => {
      if (button) button.hidden = this.images.length < 2;
    });

    this.images.forEach((el, i) => el.addEventListener('click', (e) => {
      if (e.ctrlKey || e.metaKey || e.shiftKey || e.altKey) return;
      e.preventDefault();
      this.openIndex(i);
    }));
    this.root.addEventListener('click', (e) => { if (e.target === this.root) this.close(); });
    document.addEventListener('keydown', (e) => {
      if (this.root.hidden) return;
      if (e.key === 'Tab') {
        const buttons = [this.btnClose, this.btnPrev, this.btnNext].filter(button => button && !button.hidden);
        const first = buttons[0];
        const last = buttons[buttons.length - 1];
        if (e.shiftKey && document.activeElement === first) {
          e.preventDefault();
          last.focus();
        } else if (!e.shiftKey && document.activeElement === last) {
          e.preventDefault();
          first.focus();
        }
      }
      if (['Escape', 'ArrowLeft', 'ArrowRight'].includes(e.key)) e.preventDefault();
      if (e.key === 'Escape') this.close();
      if (this.nav && e.key === 'ArrowLeft')  this.prev();
      if (this.nav && e.key === 'ArrowRight') this.next();
    });
    this.btnPrev?.addEventListener('click', () => this.prev());
    this.btnNext?.addEventListener('click', () => this.next());
  }

  openIndex(i) {
    if (!this.images[i]) return;
    const wasHidden = this.root.hidden;
    if (wasHidden) {
      this.previousFocus = document.activeElement;
      this.previousOverflow = document.body.style.overflow;
      document.body.style.overflow = 'hidden';
    }
    this.index = i;
    const el = this.images[this.index];
    const thumbnail = el.querySelector('img') || el;
    this.img.src = el.href || thumbnail.currentSrc || thumbnail.src;
    this.img.alt = thumbnail.alt || '';
    this.counter.textContent = `${i + 1} / ${this.images.length}`;
    this.root.hidden = false;
    this.root.classList.add('is-open');
    if (wasHidden) this.btnClose.focus();
  }

  next() {
    if (!this.nav) return;
    this.index = (this.index + 1) % this.images.length;
    this.openIndex(this.index);
  }

  prev() {
    if (!this.nav) return;
    this.index = (this.index - 1 + this.images.length) % this.images.length;
    this.openIndex(this.index);
  }

  close() {
    if (this.root.hidden) return;
    this.root.classList.remove('is-open');
    this.root.hidden = true;
    this.img.removeAttribute('src');
    document.body.style.overflow = this.previousOverflow;
    this.previousFocus?.focus();
  }
}
