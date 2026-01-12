class Gallery {
  constructor(root, { start = 0, loop = true, auto = 0, navRoot = null } = {}) {
    this.root  = typeof root === 'string' ? document.querySelector(root) : root;
    if (!this.root) throw new Error('Gallery root not found');

    this.track  = this.root.querySelector('.gallery__slides');
    this.slides = Array.from(this.root.querySelectorAll('.gallery__slides > .gallery__slide'));
    if (!this.track || this.slides.length === 0) throw new Error('Slides not found');

    const nav = navRoot || this.root;

    this.prevBtn = nav.querySelector('.gallery__btn_type_prev');
    this.nextBtn = nav.querySelector('.gallery__btn_type_next');

    this.loop = loop;
    this.auto = auto;
    this.timer = null;

    this.i = start || 0;

    this._measure();

    this._bind();
    this.i = this._clampIndex(this.i);
    this._update();
    if (this.auto > 0) this.play();
  }

  _measure() {
    const cs = getComputedStyle(this.root);
    const pv = parseInt((cs.getPropertyValue('--per-view') || '1').trim(), 10);
    this.perView = Number.isFinite(pv) && pv > 0 ? Math.min(pv, this.slides.length) : 1;

    const gapStr = (cs.getPropertyValue('--gap') || '0').trim();
    this.gap = parseFloat(gapStr) || 0;

    this.viewportW = this.root.clientWidth;

    this.slideW = (this.viewportW - (this.perView - 1) * this.gap) / this.perView;

    this.maxI = Math.max(0, this.slides.length - this.perView);
  }

  _offsetPx(index) {
    return index * (this.slideW + this.gap);
  }

  _clampIndex(idx) {
    if (this.loop) {
      const span = this.maxI + 1;
      return ((idx % span) + span) % span;
    }
    return Math.max(0, Math.min(idx, this.maxI));
  }

  _update() {
    const prevPerView = this.perView;
    const prevGap = this.gap;
    const prevVW = this.viewportW;

    this._measure();

    if (this.perView !== prevPerView || this.gap !== prevGap || this.viewportW !== prevVW) {
      this.i = Math.min(this.i, this.maxI);
    }

    const x = this._offsetPx(this.i);
    this.track.style.transform = `translateX(-${x}px)`;

    if (this.prevBtn) this.prevBtn.disabled = !this.loop && this.i === 0;
    if (this.nextBtn) this.nextBtn.disabled = !this.loop && this.i === this.maxI;
  }

  next() {
    this.i = (this.i < this.maxI) ? this.i + 1 : (this.loop ? 0 : this.maxI);
    this._bump(); this._update();
  }
  prev() {
    this.i = (this.i > 0) ? this.i - 1 : (this.loop ? this.maxI : 0);
    this._bump(); this._update();
  }

  play() { this.stop(); if (this.auto > 0) this.timer = setInterval(() => this.next(), this.auto); }
  stop() { if (this.timer) clearInterval(this.timer); this.timer = null; }
  _bump() { if (this.auto > 0) this.play(); }

  _bind() {

    this._onPrev = () => this.prev();
    this._onNext = () => this.next();
    this.prevBtn?.addEventListener('click', this._onPrev);
    this.nextBtn?.addEventListener('click', this._onNext);

    if (!this.root.hasAttribute('tabindex')) this.root.setAttribute('tabindex', '0');
    this._onKey = (e) => {
      if (e.key === 'ArrowLeft') this.prev();
      if (e.key === 'ArrowRight') this.next();
    };
    this.root.addEventListener('keydown', this._onKey);

    let x0 = null;
    this._touchStart = (e) => (x0 = e.touches[0].clientX);
    this._touchEnd = (e) => {
      if (x0 === null) return;
      const dx = e.changedTouches[0].clientX - x0;
      x0 = null;
      if (Math.abs(dx) < 30) return;
      dx > 0 ? this.prev() : this.next();
    };
    this.root.addEventListener('touchstart', this._touchStart, { passive: true });
    this.root.addEventListener('touchend', this._touchEnd);

    this._onResize = () => this._update();
    window.addEventListener('resize', this._onResize, { passive: true });
  }

  destroy() {
    this.stop();
    this.prevBtn?.removeEventListener('click', this._onPrev);
    this.nextBtn?.removeEventListener('click', this._onNext);
    this.root.removeEventListener('keydown', this._onKey);
    this.root.removeEventListener('touchstart', this._touchStart);
    this.root.removeEventListener('touchend', this._touchEnd);
    window.removeEventListener('resize', this._onResize);
  }
}
