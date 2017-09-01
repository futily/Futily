import Vue from 'vue'
import Component from 'vue-class-component'
import { mapGetters } from 'vuex'

import * as types from '../squads/types'

@Component({
  props: {
    player: {
      type: Object
    },
    size: {
      type: String,
      default: 'small'
    },
    position: {
      type: String
    },
    index: {
      type: Number
    },
    showChemistry: {
      type: Boolean,
      default: false
    }
  },

  computed: {
    ...mapGetters({
      getPlayer: types.GET_PLAYER,
      getPlayerChemistry: types.GET_PLAYER_CHEMISTRY
    })
  }
})
export class Card extends Vue {
  render () {
    /* eslint-disable indent */
    const position =
      this.index && this.index >= 0
        ? this.getPlayer({ index: this.index }).positions.actual
        : this.player.position

    return (
      <a
        class={[
          'plyr-Card',
          `plyr-Card-${this.size}`,
          `plyr-Card-${this.player.color}`
        ]}
        href={this.player.url}
      >
        <header class='plyr-Card_Header'>
          <div class='plyr-Card_Meta'>
            <span class='plyr-Card_Rating'>
              {this.player.rating}
            </span>
            <span class='plyr-Card_Position'>
              {position}
            </span>
            <img
              alt=''
              src={`/static/ea-images/clubs/${this.player.club.ea_id}.png`}
              class='plyr-Card_Club'
            />
            <img
              alt=''
              src={`/static/ea-images/nations/${this.player.nation.ea_id}.png`}
              class='plyr-Card_Nation'
            />
          </div>

          <img
            alt=''
            src={`/static/ea-images/players/${this.player.ea_id}.png`}
            class='plyr-Card_Image'
          />
        </header>

        <p class='plyr-Card_Name'>
          {this.player.name}
        </p>

        <div class='plyr-Card_Body'>
          {this.player.stats.map((stat, index) => {
            const key = stat[0]
            const value = stat[1]

            return (
              <div class={['plyr-Card_Stat', `plyr-Card_Stat-${index}`]}>
                <span class='plyr-Card_StatValue'>
                  {value}
                </span>
                <span class='plyr-Card_StatKey'>
                  {key}
                </span>
              </div>
            )
          })}
        </div>

        {this.showChemistry
          ? <footer class='plyr-Card_Footer'>
              <div class='plyr-Card_Chemistry'>
                <span class='plyr-Card_ChemistryLabel'>Chem:</span>
                <span class='plyr-Card_ChemistryValue'>
                  {this.getPlayerChemistry({ index: this.index })}
                </span>
              </div>
            </footer>
          : ''}
      </a>
    )
  }
}
