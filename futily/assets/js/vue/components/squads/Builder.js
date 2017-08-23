import { mapActions, mapGetters, mapMutations } from 'vuex'
import { debounce, map, reduce } from 'lodash'

import * as types from './types'
import Player from './Player'
import eaFormationMap from './utils/eaFormationMap'

export default {
  components: {
    Player
  },

  props: {
    formationChoices: {
      type: Object,
      required: true
    },
    page: {
      type: Number,
      required: true
    }
  },

  data () {
    return {
      formFields: {
        formation: 'text',
        chemistry: 'number',
        rating: 'number',
        attack: 'number',
        midfield: 'number',
        defence: 'number',
        pace: 'number',
        shooting: 'number',
        passing: 'number',
        dribbling: 'number',
        defending: 'number',
        physical: 'number'
      },
      searchResults: [],
      webAppLink: ''
    }
  },

  mounted () {
    this.setFormation({ formation: '442' })
  },

  computed: {
    ...mapGetters({
      getName: types.GET_NAME,
      getFormation: types.GET_FORMATION,
      getPlayers: types.GET_PLAYERS,
      getSearch: types.GET_SEARCH,
      getChemistry: types.GET_CHEMISTRY,
      getRating: types.GET_RATING,
      getAttack: types.GET_ATTACK,
      getMidfield: types.GET_MIDFIELD,
      getDefence: types.GET_DEFENCE,
      getPace: types.GET_PACE,
      getShooting: types.GET_SHOOTING,
      getPassing: types.GET_PASSING,
      getDribbling: types.GET_DRIBBLING,
      getDefending: types.GET_DEFENDING,
      getPhysical: types.GET_PHYSICAL,
      getPlayerObjectIds: types.GET_PLAYER_OBJECT_IDS,
      playersForForm: types.PLAYERS_FOR_FORM
    }),

    formations () {
      return Object.keys(this.formationChoices).sort().map(e => {
        return [e, this.formationChoices[e]]
      })
    }
  },

  watch: {
    'getSearch.open' (val) {
      if (val) this.$nextTick(() => this.$refs.searchInput.focus())
    }
  },

  methods: {
    ...mapActions({
      setFormation: types.SET_FORMATION,
      setPlayer: types.SET_PLAYER
    }),

    ...mapMutations({
      setName: types.SET_NAME,
      setSearch: types.SET_SEARCH
    }),

    handleSave (e) {
      e.preventDefault()

      const form = e.target
      const formData = new FormData(form)

      this.$http
        .post(form.action, formData, {
          xsrfCookieName: 'csrftoken',
          xsrfHeaderName: 'X-CSRFToken'
        })
        .then(res => {
          console.log(res)
        })
        .catch(err => {
          console.log(err.response)
        })
    },

    handleSearch (e) {
      const { value } = e.target
      this.sync('searchTerm', value)

      if (value.length > 2) {
        this.$http.get(`/api/players?query=${value}`).then(response => {
          const { data } = response
          const { results } = data

          this.searchResults = results
        })
      }
    },

    handleSearchResultsClick ($event, player) {
      this.setPlayer({ group: 'team', index: this.getSearch.position, player })
      this.$refs.searchInput.value = ''
      this.setSearch({ open: false })

      this.searchResults = []
    },

    async handleWebAppImport () {
      const link = this.webAppLink

      if (
        !link.startsWith(
          'https://www.easports.com/uk/fifa/ultimate-team/web-app/show-off'
        )
      ) {
        alert('Please provide a valid link')

        return
      }

      const id = link
        .replace(
          'https://www.easports.com/uk/fifa/ultimate-team/web-app/show-off?showoffId=',
          ''
        )
        .split(':')[0]

      const response = await this.$http.get(`/squads/builder/import/${id}`)
      const { players, squad } = response.data

      this.setFormation({ formation: squad.formation })
      this.setName({ name: squad.title })

      const playerIds = reduce(
        players,
        (ids, player) => {
          ids += `${player.player.ea_id_base},`

          return ids
        },
        ''
      )
      const { data } = await this.$http.get(`/api/players?ids=${playerIds}`)
      map(players, player => {
        player['object'] = data.results.find(
          obj => obj.ea_id_base === player['player'].ea_id_base
        )

        this.setPlayer({
          group: player.index <= 10 ? 'team' : 'bench',
          index:
            player.index <= 10
              ? eaFormationMap[squad.formation][player.index]
              : player.index,
          player: player['object'],
          position: player['position']
        })
      })
    },

    sync (prop, value) {
      this[prop] = value
    }
  },

  render (h) {
    return (
      <div class={['bld-Builder', `bld-Builder-${this.getFormation}`]}>
        <input
          type='text'
          onInput={e => this.setName({ name: e.target.value })}
          value={this.getName}
        />
        <select
          onChange={e =>
            this.setFormation({
              formation: e.target.options[e.target.selectedIndex].value
            })}
          value={this.getFormation}
          ref='formationSelect'
        >
          {this.formations.map(formation => {
            return (
              <option value={formation[0]}>
                {formation[1]}
              </option>
            )
          })}
        </select>

        <ul>
          <li>
            Chemistry: {this.getChemistry}
          </li>
          <li>
            Rating: {this.getRating}
          </li>
          <li>
            Attack: {this.getAttack}
          </li>
          <li>
            Midfield: {this.getMidfield}
          </li>
          <li>
            Defence: {this.getDefence}
          </li>
          <li>
            Pace: {this.getPace}
          </li>
          <li>
            Shooting: {this.getShooting}
          </li>
          <li>
            Pass: {this.getPassing}
          </li>
          <li>
            Dribbling: {this.getDribbling}
          </li>
          <li>
            Defending: {this.getDefending}
          </li>
          <li>
            Physical: {this.getPhysical}
          </li>
        </ul>

        <div class='bld-Builder_Import'>
          <label>
            Web app
            <input
              type='text'
              placeholder='Web app'
              onInput={e => this.sync('webAppLink', e.target.value)}
            />
          </label>
          <button
            type='submit'
            onClick={this.handleWebAppImport}
            disabled={!this.webAppLink.length}
          >
            Import
          </button>
        </div>

        <ul class='bld-Builder_Players'>
          {Object.keys(this.getPlayers.team).map((playerKey, index) => {
            const player = this.getPlayers.team[playerKey]

            return (
              <li
                class={{
                  'bld-Builder_PlayersItem': true,
                  [`bld-Builder_PlayersItem-${player.positions.formationActual.toLowerCase()}`]:
                  Object.keys(player.player).length > 0
                }}
              >
                <Player index={index} player={player} />
              </li>
            )
          })}
        </ul>

        <input
          type='search'
          v-show={this.getSearch.open}
          placeholder='Search'
          onInput={debounce(this.handleSearch, 300)}
          ref='searchInput'
        />

        <ul v-show={this.searchResults.length > 0}>
          {this.searchResults.map(player => {
            return (
              <li onClick={e => this.handleSearchResultsClick(e, player)}>
                {player.name} ({player.rating})
              </li>
            )
          })}
        </ul>

        <form
          class='bld-Builder_Form'
          onSubmit={this.handleSave}
          action='/squads/builder/save/'
        >
          <input type='hidden' name='title' value={this.getName} />
          <input type='hidden' name='page' value={this.page} />
          <input type='hidden' name='slug' value={this.getName} />
          <input type='hidden' name='players' value={this.playersForForm} />
          {Object.keys(this.formFields).map(field => {
            return (
              <input
                type='hidden'
                name={field}
                value={
                  this[`get${field.charAt(0).toUpperCase() + field.slice(1)}`]
                }
              />
            )
          })}

          <button type='submit'>Save</button>
        </form>
      </div>
    )
  }
}
