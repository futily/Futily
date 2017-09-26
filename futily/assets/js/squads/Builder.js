import positionMap from './positionMap'
import { Player } from './Player'

export class Builder {
  constructor ({ className }) {
    const el = document.querySelector(`.${className}`)

    this.className = className

    this.els = {
      el,
      team: {
        el: el.querySelector(`.${className}_Team`),
        canvas: el.querySelector(`.${className}_Canvas`),
        players: el.querySelector(`.${className}_Players`),
        items: el.querySelectorAll(`.${className}_PlayersItem`)
      },
      form: {
        el: el.querySelector(`.${className}_Form`),
        formation: el.querySelector(`.${className} [name='formation']`),
        name: el.querySelector(`.${className} [name='name']`)
      }
    }

    this.players = {
      team: Array.from(this.els.team.items).map((el, index) => {
        return new Player({ index, el })
      })
    }

    this._formation = '442'

    this.setupListeners()

    console.log(this)
  }

  setupListeners () {
    this.els.form.formation.addEventListener('change', e => {
      const { target } = e

      this.formation = target.options[target.selectedIndex].value
    })
  }

  get formation () {
    return this._formation
  }

  set formation (val) {
    this._formation = val

    this.players.team.map((player, index) => {
      player.setPosition(
        'inBuilder',
        positionMap[this._formation]['positions'][index]
      )
      player.setPosition(
        'verbose',
        positionMap[this._formation]['verbose'][index]
      )
    })

    this.els.el.setAttribute('data-builder-formation', this._formation)
  }
}
