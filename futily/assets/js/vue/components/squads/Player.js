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
    ...mapGetters({
      getPlayerChemistry: types.GET_PLAYER_CHEMISTRY
    }),

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

    handleRemove () {
      this.removePlayer({ group: 'team', index: this.index })
    },

    handleSearch () {
      this.setSearch({ open: true, position: this.index, term: '' })
    }
  },

  render (h) {
    return (
      <div class='bld-Builder_Player'>
        {this.hasPlayer ? <Card player={this.player.player} /> : ''}
        {/* <button type="button" onClick={ this.handleSearch }>Search</button> */}
        {/* <span>{ this.player.positions.actual }</span> */}
        {/* <span>{ this.player.positions.formation }</span> */}
        {/* <span>{ this.getPlayerChemistry('team', this.index) }</span> */}
        {/* <button onClick={ this.handleRemove } type="button" v-show={ this.hasPlayer }>Remove</button> */}
      </div>
    )
  }
}
