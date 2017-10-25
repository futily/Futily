import axios from 'axios'

export class Vote {
  constructor ({ className }) {
    const el = document.querySelector(className)

    this.className = className
    this.els = {
      el,
      controls: {
        down: el.querySelector(`${className}_Control[data-action='down']`),
        up: el.querySelector(`${className}_Control[data-action='up']`)
      },
      value: el.querySelector(`${className}_Value`)
    }

    this.user = this.els.el.dataset.user
    this.object = this.els.el.dataset.object
    this.url = `${this.els.el.dataset.url}rate/`

    this.sendVote = this.sendVote.bind(this)

    this.setupListeners()
  }

  setupListeners () {
    this.els.el.addEventListener('pointerdown', this.sendVote)
  }

  async sendVote (e) {
    const target = e.target.closest(`${this.className}_Control`)

    if (Object.values(this.els.controls).includes(target) === false) return

    const { action } = target.dataset
    const { object, user } = this

    if (user === 'None') {
      Vote.handleAnonUser()

      return
    }

    try {
      const { data } = await axios.post(
        this.url,
        {
          action,
          object,
          user
        },
        {
          headers: {
            X_REQUESTED_WITH: 'XMLHttpRequest'
          }
        }
      )

      this.els.value.innerText = data.score
    } catch (e) {
      console.log(e) // eslint-disable-line no-console
    }
  }

  static handleAnonUser () {
    alert('Please log in to be able to rate.')
  }
}
