export const Slide = {
  init ({ el, initialValue, cappedValue, reverse = false }) {
    this.slideKey = el.dataset.slide;
    this.initialValue = initialValue;
    this.reverse = reverse;

    this.els = {
      el,
      container: el.closest('.frm-Range_Ranges'),
      track: el.querySelector('.frm-Slide_Track'),
      slider: el.querySelector('.frm-Slide_Slider'),
      input: document.querySelector(`[data-slide-input=${this.slideKey}]`),
      value: document.querySelector(`[data-slide-value=${this.slideKey}]`)
    };

    this._currentValue = this.els.el.classList.contains('frm-Slide-min')
      ? 45
      : 99;
    this.cappedValue = Number(cappedValue);

    this.currentValue = Number(this.initialValue);
    this.minValue = 45;
    this.maxValue = 99;
    this.valueRange = this.maxValue - this.minValue;
    this.layerX = null;
    this.layerY = null;
    this.trackLength = this.els.track.offsetWidth;
    this.sliderSize = this.els.slider.offsetWidth;
    this.offsetTop = this.els.el.offsetTop;
    this.offsetLeft = this.els.el.offsetLeft;
    this.transformMaxPercentage = this.trackLength / this.sliderSize * 100;

    this._isActive = false;
    this.isTicking = false;

    this.setup();
    this.setupListeners();
  },

  setup () {
    this.setTransformPercentage();
    this.els.el.classList.remove('frm-Slide-loading');
  },

  setupListeners () {
    this.els.container.addEventListener('RangeUpdate', e => {
      const { value, key } = e.detail;

      if (key !== this.slideKey) {
        this.cappedValue = value;

        if (!this.reverse && this.cappedValue < this.currentValue) {
          this.currentValue = this.cappedValue;
        } else if (this.reverse && this.cappedValue > this.currentValue) {
          this.currentValue = this.cappedValue;
        }
      }
    });

    this.els.el.addEventListener('pointerdown', this.onPointerDown.bind(this));
    document.addEventListener('pointermove', this.onPointerMove.bind(this));
    document.addEventListener('pointerup', this.onPointerUp.bind(this));
  },

  onPointerDown (evt) {
    evt.preventDefault();

    this.layerX = evt.layerX;
    this.layerY = evt.layerY;

    this.isActive = true;
    this.requestTick();
  },

  onPointerMove (evt) {
    this.layerX = evt.layerX;
    this.layerY = evt.layerY;

    if (this.isActive) this.requestTick();
  },

  onPointerUp () {
    this.isActive = false;
  },

  setTransformPercentage () {
    const percentage = (this.currentValue - this.minValue) / this.valueRange;
    const transformPercentage = this.transformMaxPercentage * percentage;

    this.els.slider.style.transform = `translateX(${transformPercentage}%)`;
  },

  requestTick () {
    if (!this.isTicking) requestAnimationFrame(this.updateEl.bind(this));

    // If a rAF is already queued we don't want to call another one
    this.isTicking = true;
  },

  updateEl () {
    // Reset the tick so we can capture the next onScroll
    this.isTicking = false;

    // Do fun stuffs here
    const relativeX = this.layerX - this.offsetLeft;
    const startPoint = 20;
    const slidePercentage = (relativeX - startPoint) / this.trackLength * 100;
    let percentage;

    if (slidePercentage <= 0) {
      percentage = 0;
    } else if (slidePercentage >= 100) {
      percentage = 100;
    } else {
      percentage = slidePercentage;
    }

    this.currentValue = Math.round(
      this.minValue + this.valueRange * (percentage / 100)
    );
  },

  get currentValue () {
    return this._currentValue;
  },

  set currentValue (val) {
    let value;

    if (!this.reverse) {
      value = val > this.cappedValue ? this.cappedValue : val;
    } else {
      value = val < this.cappedValue ? this.cappedValue : val;
    }

    this._currentValue = value;

    this.setTransformPercentage();

    this.els.value.innerText = value;
    this.els.input.value = value;

    if (value <= 64) {
      this.els.el.setAttribute('data-color', 'bronze');
    } else if (value <= 74) {
      this.els.el.setAttribute('data-color', 'silver');
    } else {
      this.els.el.setAttribute('data-color', 'gold');
    }
  },

  get isActive () {
    return this._isActive;
  },

  set isActive (val) {
    this._isActive = val;

    if (!val) {
      const evt = new CustomEvent('RangeUpdate', {
        detail: {
          value: this.currentValue,
          key: this.slideKey
        },
        bubbles: true
      });
      this.els.el.dispatchEvent(evt);
    }
  }
};
