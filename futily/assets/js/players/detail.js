import {
  CARD_RATING_BREAKDOWN,
  CHEM_STYLE_MAX_RATING_BOOST,
  INGAME_STATS,
  POSITIONS,
  RATING_PER_POSITION
} from './constants';
import { getRatingGradeVariable, getPositionGradeVariable } from './utils';

export class CardSelector {
  constructor () {
    if (!document.querySelector('.plyr-CardSelector_Variants')) return;

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
        club: document.querySelector('.plyr-Card_Club'),
        image: document.querySelector('.plyr-Card_Image')
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
    };
    this.baseCssClass = 'plyr-Card plyr-Card-large';
    this.initialData = this.els.card.container.dataset.cardData;

    this.setupListeners();
  }

  setupListeners () {
    this.els.variantsContainer.addEventListener('pointerover', e => {
      if (this.els.variants.includes(e.target)) {
        this.setCard(e.target.dataset.cardData);
        this.compareRatings(e.target.dataset.cardData);
      }
    });

    this.els.variantsContainer.addEventListener('pointerleave', () => {
      this.clearCard();
    });

    Array.from(this.els.actions).forEach(action => {
      const isUp = action.className.includes('-up');

      action.addEventListener('pointerdown', () => {
        this.els.variantsContainer.scrollTop = isUp
          ? 0
          : this.els.variantsContainer.scrollHeight;
      });
    });
  }

  clearCard () {
    this.setCard(this.initialData);
    [1, 2, 3, 4, 5, 6].forEach(index => {
      const el = this.els.ratings[`att${index}Difference`];

      el.innerText = '';
      el.classList.remove(
        'plyr-FutilyRatings_ValueDifference-positive',
        'plyr-FutilyRatings_ValueDifference-negative'
      );
    });
  }

  setCard (data) {
    const json = JSON.parse(data);

    this.els.card.container.className = `${this
      .baseCssClass} plyr-Card-${json.color}`;
    this.els.card.rating.innerText = json.rating;
    this.els.card.position.innerText = json.position;
    this.els.card.att1.innerText = json.card_att_1;
    this.els.card.att2.innerText = json.card_att_2;
    this.els.card.att3.innerText = json.card_att_3;
    this.els.card.att4.innerText = json.card_att_4;
    this.els.card.att5.innerText = json.card_att_5;
    this.els.card.att6.innerText = json.card_att_6;
    this.els.card.club.src = `/static/ea-images/clubs/${json.club.ea_id}.png`;
    this.els.card.image.src = `/static/ea-images/players/${json.ea_id}.png`;
  }

  compareRatings (data) {
    const json = JSON.parse(data);
    const initialJson = JSON.parse(this.initialData);
    [
      json.card_att_1,
      json.card_att_2,
      json.card_att_3,
      json.card_att_4,
      json.card_att_5,
      json.card_att_6
    ].forEach((val, index) => {
      const differenceEl = this.els.ratings[`att${index + 1}Difference`];
      const difference = val - initialJson[`card_att_${index + 1}`];
      const isPositive = difference > 0;

      differenceEl.innerText = difference;
      differenceEl.classList.toggle(
        'plyr-FutilyRatings_ValueDifference-positive',
        isPositive
      );
      differenceEl.classList.toggle(
        'plyr-FutilyRatings_ValueDifference-negative',
        !isPositive
      );
    });
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
    };

    this.teamChem = 100;
    this.individualChem = 10;

    this._activeStyle = null;

    this.ingameRatings = this.getIngameRatings();
    this.cardRatings = this.getCardRatings();

    this.handlePointerDown = this.handlePointerDown.bind(this);

    this.setup();
    this.setupListeners();
  }

  setup () {
    const positionalRatings = this.getPositionalRatings();

    this.positions = this.getPositions(positionalRatings);

    // This will "run" the set stuff on rating
    Object.values(this.positions).forEach(obj => {
      obj.rating = obj.rating;
    });
  }

  setupListeners () {
    this.els.chemStyles.container.addEventListener(
      'pointerdown',
      this.handlePointerDown
    );
  }

  getCardRatings () {
    return Array.from(this.els.base.group).reduce((accumulator, el) => {
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
          return this._rating;
        },
        set rating (val) {
          this._previousRating = this._rating;
          this._rating = val < this.base ? this.base : val;

          // This is used for setting the rating colour via CSS variable
          const statGrade = getRatingGradeVariable(this._rating);

          Object.values(this.els.difference).forEach(el => {
            // Set the difference text on all our difference elements
            el.innerText = this.difference ? `(+${this.difference})` : '';
          });

          Object.values(this.els.value).forEach(el => {
            // Set the grade colour variable
            el.style.setProperty(statGrade.property, statGrade.value);

            // If the element is the groups bar, we need to set the width, otherwise we change the
            // rating text
            if (el.nodeName === 'rect') {
              el.setAttribute('width', `${this._rating}%`);
            } else {
              el.innerText = this._rating;
            }
          });
        },
        get difference () {
          return this.rating - this.base;
        }
      };

      return accumulator;
    }, {});
  }

  getIngameRatings () {
    return Array.from(this.els.base.ingame).reduce((accumulator, el) => {
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
          return this._rating;
        },
        set rating (val) {
          this._previousRating = this._rating;
          this._rating = val;

          // This is used for setting the rating colour via CSS variable
          const statGrade = getRatingGradeVariable(this._rating);

          this.els.difference.innerText = this.difference
            ? `(+${this.difference})`
            : '';
          this.els.value.innerText = val;
          this.els.value.style.setProperty(statGrade.property, statGrade.value);
        },
        get difference () {
          return this.rating - this.base;
        }
      };

      return accumulator;
    }, {});
  }

  getPositions (positionalRatings) {
    return Array.from(POSITIONS).reduce((accumulator, position) => {
      const el = document.querySelector(
        `.js-RPP_Position[data-rpp-position=${position}]`
      );

      accumulator[position] = {
        els: {
          el,
          label: el.querySelector('.js-RPP_PositionLabel'),
          value: el.querySelector('.js-RPP_PositionValue')
        },
        _rating: positionalRatings[position],
        base: positionalRatings[position],
        get rating () {
          return this._rating;
        },
        set rating (val) {
          this._rating = val;

          const statGrade = getPositionGradeVariable(this._rating);

          this.els.value.innerText = val;
          this.els.el.style.setProperty(statGrade.property, statGrade.value);
        }
      };

      return accumulator;
    }, {});
  }

  // Delta based
  getModificationFunction (modifier, individualChem) {
    if (individualChem === 0) {
      return max => -25;
    } else if (modifier < 0) {
      return max => modifier / 2;
    } else {
      return max => max * modifier / 50;
    }
  }

  normalize (val) {
    const clean = Math.round(val * 10) / 10;

    return Math.max(10, Math.min(99, Math.round(clean)));
  }

  getDeltas (style) {
    const teamChem = Math.max(0, Math.min(100, this.teamChem));
    const individualChem = Math.max(0, Math.min(10, this.individualChem));
    const modifier = 0.25 * teamChem + 7.5 * individualChem - 50;
    const modify = this.getModificationFunction(modifier, individualChem);
    const maximums =
      CHEM_STYLE_MAX_RATING_BOOST[style] || CHEM_STYLE_MAX_RATING_BOOST.basic;

    return Object.values(maximums).reduce((accumulator, val, position) => {
      accumulator[position] = modify(val);

      return accumulator;
    }, {});
  }

  getBasePositionalRatings () {
    return Object.entries(this.positions).reduce((accumulator, tuple) => {
      const [position, obj] = tuple;

      accumulator[position] = obj.base;

      return accumulator;
    }, {});
  }

  getPositionalRatings () {
    return Object.entries(RATING_PER_POSITION).reduce((accumulator, tuple) => {
      const [position, stats] = tuple;
      const rating = Array.from(INGAME_STATS).reduce(
        (sum, stat) => sum + stats[stat] * this.ingameRatings[stat].rating,
        0
      );

      accumulator[position] = Math.round(rating);

      return accumulator;
    }, {});
  }

  updateCardRatings (style) {
    if (style) {
      Object.entries(CARD_RATING_BREAKDOWN).forEach(tuple => {
        const [attr, obj] = tuple;

        let coreFinal = 0;

        Object.entries(obj).forEach(tuple => {
          const [field, weight] = tuple;

          coreFinal += this.ingameRatings[field].rating * weight;
        });

        this.cardRatings[attr].rating = Math.round(coreFinal);
      });
    } else {
      Object.values(this.cardRatings).forEach(obj => {
        obj.rating = obj.base;
      });
    }
  }

  updateIngameRatings (style) {
    if (style) {
      const deltas = this.getDeltas(style);

      Object.values(this.ingameRatings).forEach((obj, key) => {
        obj.rating = this.normalize(obj.base + deltas[key]);
      });
    } else {
      Object.values(this.ingameRatings).forEach(obj => {
        obj.rating = obj.base;
      });
    }
  }

  updatePositionalRatings (ratings) {
    Object.entries(ratings).forEach(tuple => {
      const [position, val] = tuple;

      this.positions[position].rating = val;
    });
  }

  handlePointerDown (e) {
    const wantedTarget = e.target.closest('.js-RPP_ChemStyle');
    const style = wantedTarget.dataset.rppChemStyle;

    this.activeStyle = style === this.activeStyle ? null : style;
  }

  get activeStyle () {
    return this._activeStyle;
  }

  set activeStyle (val) {
    this._activeStyle = val;

    Array.from(this.els.chemStyles.items).forEach(item => {
      item.setAttribute(
        'aria-current',
        String(val === item.closest('.js-RPP_ChemStyle').dataset.rppChemStyle)
      );
    });

    this.updateIngameRatings(this._activeStyle);
    this.updateCardRatings(this._activeStyle);

    if (this._activeStyle) {
      this.updatePositionalRatings(this.getPositionalRatings());
    } else {
      this.updatePositionalRatings(this.getBasePositionalRatings());
    }
  }
}
