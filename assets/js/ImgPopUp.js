class ImgPopUp {
  constructor(targets = 'img', { nav = true } = {}) {
    this.images = typeof targets === 'string'
      ? Array.from(document.querySelectorAll(targets))
      : Array.from(targets);

    this.nav = nav;
    this.index = -1;

    // Попап
    this.root = document.createElement('div');
    this.root.className = 'imgpop';
    this.root.hidden = true;

    const navHtml = this.nav
      ? `<button class="imgpop__btn imgpop__btn--prev" aria-label="Prev"></button>
         <button class="imgpop__btn imgpop__btn--next" aria-label="Next"></button>`
      : ``;

    this.root.innerHTML = `
      <img class="imgpop__img" alt="">
      ${navHtml}
    `;
    document.body.appendChild(this.root);

    this.img  = this.root.querySelector('.imgpop__img');
    this.btnPrev = this.root.querySelector('.imgpop__btn--prev');
    this.btnNext = this.root.querySelector('.imgpop__btn--next');

    this.images.forEach((el, i) => el.addEventListener('click', () => this.openIndex(i)));
    this.root.addEventListener('click', (e) => { if (e.target === this.root) this.close(); });
    document.addEventListener('keydown', (e) => {
      if (this.root.hidden) return;
      if (e.key === 'Escape') this.close();
      if (this.nav && e.key === 'ArrowLeft')  this.prev();
      if (this.nav && e.key === 'ArrowRight') this.next();
    });
    this.btnPrev?.addEventListener('click', () => this.prev());
    this.btnNext?.addEventListener('click', () => this.next());
  }

  openIndex(i) {
    this.index = i;
    const el = this.images[this.index];
    this.img.src = el.currentSrc || el.src;
    this.img.alt = el.alt || '';
    this.root.hidden = false;
    requestAnimationFrame(() => this.root.classList.add('is-open'));
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
    this.root.classList.remove('is-open');
    this.root.addEventListener('transitionend', () => { this.root.hidden = true; this.img.src=''; }, { once: true });
  }
}
