export class FloatingLabel {
  constructor ({ el }) {
    this.className = 'js-FloatingLabel'

    this.els = {
      el,
      label: el.querySelector(`.${this.className}_Label`),
      input: el.querySelector(`.${this.className}_Input`)
    }

    this.shouldBeFloated = this.els.input.value.length > 0

    this.setupListeners()
  }

  setupListeners () {
    this.els.input.addEventListener('focus', () => {
      this.shouldBeFloated = true
    })

    this.els.input.addEventListener('blur', e => {
      this.shouldBeFloated = e.target.value.length > 0
    })
  }

  get shouldBeFloated () {
    return this._shouldBeFloated
  }

  set shouldBeFloated (val) {
    this._shouldBeFloated = val

    this.els.el.classList.toggle(`${this.className}-active`, val)
  }
}
