import { Builder } from './Builder'
import { ChemistryRequirement, RatingRequirement } from './requirements'

export class Challenge extends Builder {
  constructor ({ className, isEditable }) {
    super({ className, isEditable })

    const el = document.querySelector(`.${className}`)

    this.ajaxSave = !el.classList.contains('js-Builder-noAjax')
    this.className = className

    this.els = Object.assign(this.els, {
      requirements: {
        el: el.querySelector('.js-Builder_Requirements'),
        items: el.querySelectorAll('.js-Builder_Requirement')
      }
    })

    this.requirements = {
      // These will be looped over and called on player insertion, so we can keep the requirements
      // up to date
      fncs: [],
      // These will be the "values" of each requirement
      stats: {},
      get passed () {
        return (
          Object.keys(this.stats).length > 0 &&
          Object.values(this.stats).filter(stat => {
            return stat.passed
          }).length === Object.keys(this.stats).length
        )
      }
    }

    this.setupRequirements()
  }

  setupRequirements () {
    const requirementSchema = Array.from(
      this.els.requirements.items
    ).map(item => ({
      el: item,
      data: JSON.parse(item.dataset.requirement)
    }))

    requirementSchema.forEach(requirement => this.setupRequirement(requirement))
  }

  setupRequirement (requirement) {
    const { el } = requirement
    const { scope, type, value } = requirement.data

    if (type === 'chemistry') {
      this.requirements.stats.chemistry = new ChemistryRequirement({
        el,
        scope,
        value
      })
      this.requirements.fncs.push(
        this.requirements.stats.chemistry.calculateValue.bind(
          null,
          this.players
        )
      )
    } else if (type === 'rating') {
      this.requirements.stats.rating = new RatingRequirement({
        el,
        scope,
        value
      })
      this.requirements.fncs.push(
        this.requirements.stats.rating.calculateValue.bind(null, this.players)
      )
    }
  }

  insertPlayer ({ data, element, index }) {
    super.insertPlayer({ data, element, index })

    this.requirements.fncs.forEach(fnc => fnc())
  }
}
