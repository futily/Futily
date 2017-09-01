import Vue from 'vue'
import Component from 'vue-class-component'
import { mapActions, mapMutations } from 'vuex'

import { Card } from '../players/Card'
import * as types from './types'

@Component({
  components: {
    Card
  },

  props: {
    index: {
      type: Number,
      required: true
    },
    player: {
      type: Object,
      required: true
    }
  },

  methods: {
    ...mapActions({
      removePlayer: types.REMOVE_PLAYER
    }),

    ...mapMutations({
      setSearch: types.SET_SEARCH
    })
  }
})
export class Player extends Vue {
  handleRemove ($evt) {
    $evt.stopPropagation()

    this.removePlayer({ group: 'team', index: this.index })
  }

  get hasPlayer () {
    return Object.keys(this.player.player).length > 0
  }

  render () {
    /* eslint-disable indent */
    return (
      <div class='bld-Builder_Player'>
        {this.hasPlayer
          ? <Card
              player={this.player.player}
              index={this.index}
              showChemistry={true}
            />
          : ''}
        <button
          class='bld-Builder_PlayerRemove'
          onClick={this.handleRemove}
          type='button'
          v-show={this.hasPlayer}
        >
          Remove
        </button>
      </div>
    )
  }
}
