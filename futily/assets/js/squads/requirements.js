import { getAverageStat } from './utils'

class Requirement {
  constructor ({ el, scope, value }) {
    this.els = {
      el,
      data: el.querySelector('.js-Builder_RequirementData'),
      current: el.querySelector('.js-Builder_RequirementCurrent')
    }

    this.required = value
    this.scope = scope
    this.value = value

    this.calculateValue = this.calculateValue.bind(this)
  }

  calculateValue () {
    throw new Error('This method needs to be implemented')
  }

  setValue (val) {
    this.value = val

    this.els.current.innerText = val
  }

  get passed () {
    return this.scope === 'gte'
      ? this.value >= this.required
      : this.scope === 'lte'
        ? this.value <= this.required
        : this.value === this.required
  }
}

export class ChemistryRequirement extends Requirement {
  calculateValue (players) {
    this.setValue(
      Math.min(
        Math.max(
          0,
          players.team.reduce((acc, player) => {
            acc += player.chemistry.total

            return acc
          }, 0)
        ),
        100
      )
    )
  }
}

export class RatingRequirement extends Requirement {
  calculateValue (players) {
    this.setValue(
      getAverageStat({
        players: players.team,
        stat: 'rating',
        includeGk: true
      })
    )
  }
}
