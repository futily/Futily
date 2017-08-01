import { map } from 'lodash'

export class CardSelector {
  constructor () {
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
        att6: document.querySelector('.plyr-Card_Stat-6 .plyr-Card_StatValue')
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
