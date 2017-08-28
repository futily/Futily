import { mapActions, mapGetters, mapMutations } from 'vuex'

import Card from '../players/Card'
import * as types from './types'

export default {
  name: 'Player',

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

  computed: {
    hasPlayer () {
      return Object.keys(this.player.player).length > 0
    }
  },

  methods: {
    ...mapActions({
      removePlayer: types.REMOVE_PLAYER
    }),

    ...mapMutations({
      setSearch: types.SET_SEARCH
    }),

    handleRemove ($evt) {
      $evt.stopPropagation()

      this.removePlayer({ group: 'team', index: this.index })
    }
  },

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
