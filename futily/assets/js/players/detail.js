import axios from 'axios'
import { map, reduce } from 'lodash'

import {
  CARD_RATING_BREAKDOWN,
  CHEM_STYLE_MAX_RATING_BOOST,
  INGAME_STATS,
  POSITIONS,
  RATING_PER_POSITION
} from './constants'
import { getRatingGradeVariable, getPositionGradeVariable } from './utils'

export class CardSelector {
  constructor () {
    if (!document.querySelector('.plyr-CardSelector_Variants')) return

    this.els = {
      el: document.querySelector('.plyr-CardSelector'),
      actions: document.querySelectorAll('.plyr-CardSelector_Action'),
      variantsContainer: document.querySelector('.plyr-CardSelector_Variants'),
      variants: Array.from(
        document.querySelectorAll('.plyr-CardSelector_Variant')
      ),
      cardContainer: document.querySelector('.plyr-CardSelector_Card'),
      card: {
        container: document.querySelector('.plyr-Card'),
        rating: document.querySelector('.plyr-Card_Rating'),
        position: document.querySelector('.plyr-Card_Position'),
        att1: document.querySelector('.plyr-Card_Stat-1 .plyr-Card_StatValue'),
        att2: document.querySelector('.plyr-Card_Stat-2 .plyr-Card_StatValue'),
        att3: document.querySelector('.plyr-Card_Stat-3 .plyr-Card_StatValue'),
        att4: document.querySelector('.plyr-Card_Stat-4 .plyr-Card_StatValue'),
        att5: document.querySelector('.plyr-Card_Stat-5 .plyr-Card_StatValue'),
        att6: document.querySelector('.plyr-Card_Stat-6 .plyr-Card_StatValue'),
        club: document.querySelector('.plyr-Card_Club')
      },
      ratings: {
        att1: document.querySelector(
          '.plyr-FutilyRatings_Item-1 .plyr-FutilyRatings_Value'
        ),
        att1Difference: document.querySelector(
          '.plyr-FutilyRatings_Item-1 .plyr-FutilyRatings_ValueDifference'
        ),
        att2: document.querySelector(
          '.plyr-FutilyRatings_Item-2 .plyr-FutilyRatings_Value'
        ),
        att2Difference: document.querySelector(
          '.plyr-FutilyRatings_Item-2 .plyr-FutilyRatings_ValueDifference'
        ),
        att3: document.querySelector(
          '.plyr-FutilyRatings_Item-3 .plyr-FutilyRatings_Value'
        ),
        att3Difference: document.querySelector(
          '.plyr-FutilyRatings_Item-3 .plyr-FutilyRatings_ValueDifference'
        ),
        att4: document.querySelector(
          '.plyr-FutilyRatings_Item-4 .plyr-FutilyRatings_Value'
        ),
        att4Difference: document.querySelector(
          '.plyr-FutilyRatings_Item-4 .plyr-FutilyRatings_ValueDifference'
        ),
        att5: document.querySelector(
          '.plyr-FutilyRatings_Item-5 .plyr-FutilyRatings_Value'
        ),
        att5Difference: document.querySelector(
          '.plyr-FutilyRatings_Item-5 .plyr-FutilyRatings_ValueDifference'
        ),
        att6: document.querySelector(
          '.plyr-FutilyRatings_Item-6 .plyr-FutilyRatings_Value'
        ),
        att6Difference: document.querySelector(
          '.plyr-FutilyRatings_Item-6 .plyr-FutilyRatings_ValueDifference'
        )
      }
    }
    this.baseCssClass = 'plyr-Card plyr-Card-large'
    this.initialData = this.els.card.container.dataset.cardData

    this.setupListeners()
  }

  setupListeners () {
    this.els.variantsContainer.addEventListener('pointerover', e => {
      if (this.els.variants.includes(e.target)) {
        this.setCard(e.target.dataset.cardData)
        this.compareRatings(e.target.dataset.cardData)
      }
    })

    this.els.variantsContainer.addEventListener('pointerleave', () => {
      this.clearCard()
    })

    map(this.els.actions, action => {
      const isUp = action.className.includes('-up')

      action.addEventListener('pointerdown', () => {
        this.els.variantsContainer.scrollTop = isUp
          ? 0
          : this.els.variantsContainer.scrollHeight
      })
    })
  }

  clearCard () {
    this.setCard(this.initialData)
    map([1, 2, 3, 4, 5, 6], index => {
      const el = this.els.ratings[`att${index}Difference`]

      el.innerText = ''
      el.classList.remove(
        'plyr-FutilyRatings_ValueDifference-positive',
        'plyr-FutilyRatings_ValueDifference-negative'
      )
    })
  }

  setCard (data) {
    const json = JSON.parse(data)

    this.els.card.container.className = `${this
      .baseCssClass} plyr-Card-${json.color}`
    this.els.card.rating.innerText = json.rating
    this.els.card.position.innerText = json.position
    this.els.card.att1.innerText = json.card_att_1
    this.els.card.att2.innerText = json.card_att_2
    this.els.card.att3.innerText = json.card_att_3
    this.els.card.att4.innerText = json.card_att_4
    this.els.card.att5.innerText = json.card_att_5
    this.els.card.att6.innerText = json.card_att_6
    this.els.card.club.src = `/static/ea-images/clubs/${json.club.ea_id}.png`
  }

  compareRatings (data) {
    const json = JSON.parse(data)
    const initialJson = JSON.parse(this.initialData)

    map(
      [
        json.card_att_1,
        json.card_att_2,
        json.card_att_3,
        json.card_att_4,
        json.card_att_5,
        json.card_att_6
      ],
      (val, index) => {
        const differenceEl = this.els.ratings[`att${index + 1}Difference`]
        const difference = val - initialJson[`card_att_${index + 1}`]
        const isPositive = difference > 0

        differenceEl.innerText = difference
        differenceEl.classList.toggle(
          'plyr-FutilyRatings_ValueDifference-positive',
          isPositive
        )
        differenceEl.classList.toggle(
          'plyr-FutilyRatings_ValueDifference-negative',
          !isPositive
        )
      }
    )
  }
}

export class Rating {
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
    this.player = this.els.el.dataset.player
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
    const { player, user } = this

    if (user === 'None') {
      this.handleAnonUser()

      return
    }

    try {
      const { data } = await axios.post(
        this.url,
        {
          action,
          player,
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
      console.log(e)
    }
  }

  handleAnonUser () {
    alert('Please log in to be able to rate players')
  }
}

export class RPP {
  constructor () {
    this.els = {
      base: {
        group: document.querySelectorAll('.js-RPP_Base-group'),
        ingame: document.querySelectorAll('.js-RPP_Base-ingame')
      },
      chemStyles: {
        container: document.querySelector('.js-RPP_ChemStyles'),
        items: document.querySelectorAll('.js-RPP_ChemStyle')
      }
    }

    this.teamChem = 100
    this.individualChem = 10

    this._activeStyle = null

    this.ingameRatings = this.getIngameRatings()
    this.cardRatings = this.getCardRatings()

    this.handlePointerDown = this.handlePointerDown.bind(this)

    this.setup()
    this.setupListeners()
  }

  setup () {
    const positionalRatings = this.getPositionalRatings()

    this.positions = this.getPositions(positionalRatings)

    // This will "run" the set stuff on rating
    map(this.positions, obj => {
      obj.rating = obj.rating
    })
  }

  setupListeners () {
    this.els.chemStyles.container.addEventListener(
      'pointerdown',
      this.handlePointerDown
    )
  }

  getCardRatings () {
    return reduce(
      this.els.base.group,
      (accumulator, el) => {
        accumulator[el.dataset.rppField] = {
          els: {
            el,
            difference: {
              base: document.querySelector(
                `.js-RPP_Base-base[data-rpp-field="${el.dataset
                  .rppField}"] .js-RPP_BaseDifference`
              ),
              card: document.querySelector(
                `.js-RPP_Base-card[data-rpp-field="${el.dataset
                  .rppField}"] .js-RPP_CardDifference`
              ),
              group: el.querySelector('.js-RPP_GroupDifference')
            },
            value: {
              base: document.querySelector(
                `.js-RPP_Base-base[data-rpp-field="${el.dataset
                  .rppField}"] .js-RPP_BaseValue`
              ),
              card: document.querySelector(
                `.js-RPP_Base-card[data-rpp-field="${el.dataset
                  .rppField}"] .js-RPP_CardValue`
              ),
              group: el.querySelector('.js-RPP_GroupValue'),
              bar: el.querySelector('.js-RPP_Bar')
            }
          },
          base: Number(el.dataset.rppBase),
          _rating: Number(el.dataset.rppBase),
          _previousRating: Number(el.dataset.rppBase),
          get rating () {
            return this._rating
          },
          set rating (val) {
            this._previousRating = this._rating
            this._rating = val < this.base ? this.base : val

            // This is used for setting the rating colour via CSS variable
            const statGrade = getRatingGradeVariable(this._rating)

            map(this.els.difference, el => {
              // Set the difference text on all our difference elements
              el.innerText = this.difference ? `(+${this.difference})` : ''
            })

            map(this.els.value, el => {
              // Set the grade colour variable
              el.style.setProperty(statGrade.property, statGrade.value)

              // If the element is the groups bar, we need to set the width, otherwise we change the
              // rating text
              if (el.nodeName === 'rect') {
                el.setAttribute('width', `${this._rating}%`)
              } else {
                el.innerText = this._rating
              }
            })
          },
          get difference () {
            return this.rating - this.base
          }
        }

        return accumulator
      },
      {}
    )
  }

  getIngameRatings () {
    return reduce(
      this.els.base.ingame,
      (accumulator, el) => {
        accumulator[el.dataset.rppField] = {
          els: {
            el,
            difference: el.querySelector('.js-RPP_BaseDifference'),
            value: el.querySelector('.js-RPP_BaseValue')
          },
          base: Number(el.dataset.rppBase),
          _rating: Number(el.dataset.rppBase),
          _previousRating: Number(el.dataset.rppBase),
          get rating () {
            return this._rating
          },
          set rating (val) {
            this._previousRating = this._rating
            this._rating = val

            // This is used for setting the rating colour via CSS variable
            const statGrade = getRatingGradeVariable(this._rating)

            this.els.difference.innerText = this.difference
              ? `(+${this.difference})`
              : ''
            this.els.value.innerText = val
            this.els.value.style.setProperty(
              statGrade.property,
              statGrade.value
            )
          },
          get difference () {
            return this.rating - this.base
          }
        }

        return accumulator
      },
      {}
    )
  }

  getPositions (positionalRatings) {
    return reduce(
      POSITIONS,
      (accumulator, position) => {
        const el = document.querySelector(
          `.js-RPP_Position[data-rpp-position=${position}]`
        )

        accumulator[position] = {
          els: {
            el,
            label: el.querySelector('.js-RPP_PositionLabel'),
            value: el.querySelector('.js-RPP_PositionValue')
          },
          _rating: positionalRatings[position],
          base: positionalRatings[position],
          get rating () {
            return this._rating
          },
          set rating (val) {
            this._rating = val

            const statGrade = getPositionGradeVariable(this._rating)

            this.els.value.innerText = val
            this.els.el.style.setProperty(statGrade.property, statGrade.value)
          }
        }

        return accumulator
      },
      {}
    )
  }

  // Delta based
  getModificationFunction (modifier, individualChem) {
    if (individualChem === 0) {
      return max => -25
    } else if (modifier < 0) {
      return max => modifier / 2
    } else {
      return max => max * modifier / 50
    }
  }

  normalize (val) {
    const clean = Math.round(val * 10) / 10

    return Math.max(10, Math.min(99, Math.round(clean)))
  }

  getDeltas (style) {
    const teamChem = Math.max(0, Math.min(100, this.teamChem))
    const individualChem = Math.max(0, Math.min(10, this.individualChem))
    const modifier = 0.25 * teamChem + 7.5 * individualChem - 50
    const modify = this.getModificationFunction(modifier, individualChem)
    const maximums =
      CHEM_STYLE_MAX_RATING_BOOST[style] || CHEM_STYLE_MAX_RATING_BOOST.basic

    return reduce(
      maximums,
      (accumulator, val, position) => {
        accumulator[position] = modify(val)

        return accumulator
      },
      {}
    )
  }

  getBasePositionalRatings () {
    return reduce(
      this.positions,
      (accumulator, obj, position) => {
        accumulator[position] = obj.base

        return accumulator
      },
      {}
    )
  }

  getPositionalRatings () {
    return reduce(
      RATING_PER_POSITION,
      (accumulator, ratings, position) => {
        const rating = reduce(
          INGAME_STATS,
          (sum, stat) =>
            (sum += ratings[stat] * this.ingameRatings[stat].rating), // eslint-disable-line no-return-assign
          0
        )

        accumulator[position] = Math.round(rating)

        return accumulator
      },
      {}
    )
  }

  updateCardRatings (style) {
    if (style) {
      map(CARD_RATING_BREAKDOWN, (obj, attr) => {
        let coreFinal = 0

        map(obj, (weight, field) => {
          coreFinal += this.ingameRatings[field].rating * weight
        })

        this.cardRatings[attr].rating = Math.round(coreFinal)
      })
    } else {
      map(this.cardRatings, obj => {
        obj.rating = obj.base
      })
    }
  }

  updateIngameRatings (style) {
    if (style) {
      const deltas = this.getDeltas(style)

      map(this.ingameRatings, (obj, key) => {
        obj.rating = this.normalize(obj.base + deltas[key])
      })
    } else {
      map(this.ingameRatings, obj => {
        obj.rating = obj.base
      })
    }
  }

  updatePositionalRatings (ratings) {
    map(ratings, (val, position) => {
      this.positions[position].rating = val
    })
  }

  handlePointerDown (e) {
    const wantedTarget = e.target.closest('.js-RPP_ChemStyle')
    const style = wantedTarget.dataset.rppChemStyle

    this.activeStyle = style === this.activeStyle ? null : style
  }

  get activeStyle () {
    return this._activeStyle
  }

  set activeStyle (val) {
    this._activeStyle = val

    map(this.els.chemStyles.items, item => {
      item.setAttribute(
        'aria-current',
        String(val === item.closest('.js-RPP_ChemStyle').dataset.rppChemStyle)
      )
    })

    this.updateIngameRatings(val)
    this.updateCardRatings(val)

    if (val) {
      this.updatePositionalRatings(this.getPositionalRatings())
    } else {
      this.updatePositionalRatings(this.getBasePositionalRatings())
    }
  }
}
