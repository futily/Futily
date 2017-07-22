import { Slide } from './slide'

export const PlayerFilterForm = {
  init ({ el }) {
    this.el = el
    this.els = {
      resetNames: document.querySelectorAll('.js-PlayerFilter_ResetName'),
      collapse: this.el.querySelectorAll('.js-PlayerFilter_Collapse'),
      flyouts: this.el.querySelectorAll('.js-PlayerFilter_Flyout')
    }

    this.hasFlyoutOpen = false
    this.submitNeedsToBeChecked = false

    this.handleSubmit = this.handleSubmit.bind(this)

    this.setup()
    this.setupListeners()
  },

  setup () {
    this.setupRatingRange()
    this.setupCollapses()
    this.setupFlyouts()
  },

  setupListeners () {
    this.el.addEventListener('submit', this.handleSubmit)

    Array.from(this.els.resetNames).map(el => {
      el.addEventListener('change', evt => {
        const { name } = evt.target

        Array.from(this.el.querySelectorAll(`[name=${name}]`))
          .filter(nameEl => nameEl !== evt.target)
          .map(nameEl => {
            nameEl.checked = false
          })

        this.submitNeedsToBeChecked = true
      })
    })
  },

  handleSubmit (evt) {
    if (this.submitNeedsToBeChecked) evt.preventDefault()

    const formData = new FormData(this.el)
    const namesToClear = []

    for (const [key, value] of formData.entries()) {
      if (value === 'all') namesToClear.push(key)
    }

    namesToClear.map(name => {
      formData.delete(name)

      Array.from(this.el.querySelectorAll(`[name=${name}]`)).map(el => {
        el.checked = false
      })
    })

    evt.target.submit()
  },

  setupRatingRange () {
    const minSlide = this.el.querySelector('.frm-Slide-min')
    const maxSlide = this.el.querySelector('.frm-Slide-max')

    const minSlideObj = Object.create(Slide)
    const maxSlideObj = Object.create(Slide)

    minSlideObj.init({
      el: minSlide,
      initialValue: this.el.querySelector('[data-slide-input=min]').value,
      cappedValue: this.el.querySelector('[data-slide-input=max]').value
    })
    maxSlideObj.init({
      el: maxSlide,
      initialValue: this.el.querySelector('[data-slide-input=max]').value,
      cappedValue: this.el.querySelector('[data-slide-input=min]').value,
      reverse: true
    })
  },

  setupCollapses () {
    Array.from(this.els.collapse).map(el => {
      const trigger = el.querySelector('.js-PlayerFilter_CollapseToggle')

      trigger.addEventListener('click', () => {
        const expanded = el.getAttribute('aria-expanded') === 'true'

        el.setAttribute('aria-expanded', !expanded)
      })
    })
  },

  setupFlyouts () {
    Array.from(this.els.flyouts).map(el => {
      const name = el.dataset.formName
      const inputEls = Array.from(el.querySelectorAll(`[name=${name}]`))
      const trigger = el.querySelector('.js-PlayerFilter_FlyoutToggle')
      const close = el.querySelector('.js-PlayerFilter_Close')
      const clear = el.querySelector('.js-PlayerFilter_Clear')

      trigger.addEventListener('click', evt => {
        const parent = evt.target.closest('.js-PlayerFilter_Flyout')
        const expanded = el.getAttribute('aria-expanded') === 'true'

        this.hasFlyoutOpen = !expanded
        el.setAttribute('aria-expanded', !expanded)

        Array.from(this.els.flyouts).map(flyoutEl => {
          if (flyoutEl !== parent && !expanded) {
            flyoutEl.setAttribute('aria-expanded', 'false')
          }
        })
      })

      close.addEventListener('click', () =>
        el.setAttribute('aria-expanded', 'false')
      )

      clear.addEventListener('click', () => {
        inputEls.map(input => {
          input.checked = false
        })
      })
    })

    document.addEventListener('click', evt => {
      if (
        !evt.target.closest('.js-PlayerFilter_Flyout') &&
        this.hasFlyoutOpen
      ) {
        Array.from(this.els.flyouts).map(el => {
          el.setAttribute('aria-expanded', 'false')
        })
      }
    })
  }
}
