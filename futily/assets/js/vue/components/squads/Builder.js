import Vue from 'vue'
import Component from 'vue-class-component'
import { mapActions, mapGetters, mapMutations } from 'vuex'
import { map, reduce } from 'lodash'

import * as types from './types'
import eaFormationMap from './utils/eaFormationMap'
import { Team } from './Team'
import {
  getPositionGradeVariable,
  getRatingGradeVariable
} from '../../../players/utils'

@Component({
  components: {
    Team
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
      getPlayerChemistry: types.GET_PLAYER_CHEMISTRY,
      getPlayerFormationLinks: types.GET_PLAYER_FORMATION_LINKS,
      getPlayerObjectIds: types.GET_PLAYER_OBJECT_IDS,
      playersForForm: types.PLAYERS_FOR_FORM
    })
  },

  watch: {
    getFormation () {
      this.isTransitioning = true

      setTimeout(() => {
        this.isTransitioning = false
      }, 500)
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

    getRatingGradeVariable
  }
})
export class Builder extends Vue {
  formFields = {
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
  }
  isTransitioning = false
  webAppLink = ''

  mounted () {
    this.setFormation({ formation: '442' })
  }

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
  }

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
  }

  sync (prop, value) {
    this[prop] = value
  }

  get formations () {
    return Object.keys(this.formationChoices)
      .sort()
      .map(e => {
        return [e, this.formationChoices[e]]
      })
  }

  get stars () {
    if (this.getRating > 82) {
      return 5
    } else if (this.getRating > 78) {
      return 4.5
    } else if (this.getRating > 74) {
      return 4
    } else if (this.getRating > 70) {
      return 3.5
    } else if (this.getRating > 68) {
      return 3
    } else if (this.getRating > 66) {
      return 2.5
    } else if (this.getRating > 64) {
      return 2
    } else if (this.getRating > 62) {
      return 1.5
    } else if (this.getRating > 59) {
      return 1
    } else if (this.getRating > 1) {
      return 0.5
    } else {
      return 0
    }
  }

  get stats () {
    return [
      {
        label: 'Attack',
        value: this.getAttack,
        style: { '--RatingColor': getRatingGradeVariable(this.getAttack).value }
      },
      {
        label: 'Midfield',
        value: this.getMidfield,
        style: {
          '--RatingColor': getRatingGradeVariable(this.getMidfield).value
        }
      },
      {
        label: 'Defence',
        value: this.getDefence,
        style: {
          '--RatingColor': getRatingGradeVariable(this.getDefence).value
        }
      },
      {
        label: 'Pace',
        value: this.getPace,
        style: { '--RatingColor': getRatingGradeVariable(this.getPace).value }
      },
      {
        label: 'Shooting',
        value: this.getShooting,
        style: {
          '--RatingColor': getRatingGradeVariable(this.getShooting).value
        }
      },
      {
        label: 'Pass',
        value: this.getPassing,
        style: {
          '--RatingColor': getRatingGradeVariable(this.getPassing).value
        }
      },
      {
        label: 'Dribbling',
        value: this.getDribbling,
        style: {
          '--RatingColor': getRatingGradeVariable(this.getDribbling).value
        }
      },
      {
        label: 'Defending',
        value: this.getDefending,
        style: {
          '--RatingColor': getRatingGradeVariable(this.getDefending).value
        }
      },
      {
        label: 'Physical',
        value: this.getPhysical,
        style: {
          '--RatingColor': getRatingGradeVariable(this.getPhysical).value
        }
      }
    ]
  }

  render () {
    return (
      <div
        class={{
          'bld-Builder': true,
          [`bld-Builder-${this.getFormation}`]: true,
          'bld-Builder-transitioning': this.isTransitioning
        }}
      >
        <div class='bld-Builder_Body'>
          <Team isTransitioning={this.isTransitioning} />
        </div>

        <footer class='bld-Builder_Footer'>
          <div class='bld-Builder_Columns'>
            <div class='bld-Builder_Column'>
              <div class='frm-Form_Items'>
                <div class='frm-Form_Item frm-Form_Item-full frm-Form_Item-floatingLabel js-FloatingLabel js-FloatingLabel-active'>
                  <label
                    class='frm-Form_Label js-FloatingLabel_Label'
                    for='name'
                  >
                    Formation:
                  </label>

                  <select
                    class='frm-Form_Select js-FloatingLabel_Input'
                    id='formation'
                    name='formation'
                    onChange={e =>
                      this.setFormation({
                        formation:
                          e.target.options[e.target.selectedIndex].value
                      })}
                    value={this.getFormation}
                    ref='formationSelect'
                  >
                    {this.formations.map(formation => {
                      return (
                        <option value={formation[0]}>{formation[1]}</option>
                      )
                    })}
                  </select>
                </div>

                <div class='frm-Form_Item frm-Form_Item-full frm-Form_Item-floatingLabel js-FloatingLabel'>
                  <label
                    class='frm-Form_Label js-FloatingLabel_Label'
                    for='name'
                  >
                    Squad Name:
                  </label>

                  <input
                    type='text'
                    class='frm-Form_Input js-FloatingLabel_Input'
                    placeholder='Name'
                    name='name'
                    id='name'
                    onInput={e => this.setName({ name: e.target.value })}
                    value={this.getName}
                  />
                </div>
              </div>
            </div>

            <div class='bld-Builder_Column'>
              <div class='bld-Builder_Stats'>
                <div class='bld-Stats'>
                  <ul class='bld-Stats_Items'>
                    <li class='bld-Stats_Item'>
                      <span class='bld-Stats_Label'>Rating:</span>
                      <span
                        class='bld-Stats_Value'
                        style={{
                          '--RatingColor': getRatingGradeVariable(
                            this.getRating
                          ).value
                        }}
                      >
                        {this.getRating}
                      </span>
                    </li>

                    <li class='bld-Stats_Item'>
                      <span class='bld-Stats_Label'>Chemistry:</span>
                      <span
                        class='bld-Stats_Value'
                        style={{
                          '--RatingColor': getPositionGradeVariable(
                            this.getChemistry
                          ).value
                        }}
                      >
                        {this.getChemistry}
                      </span>
                    </li>
                  </ul>
                </div>
              </div>

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

                <form
                  class='bld-Builder_Form'
                  onSubmit={this.handleSave}
                  action='/squads/builder/save/'
                >
                  <input type='hidden' name='title' value={this.getName} />
                  <input type='hidden' name='page' value={this.page} />
                  <input type='hidden' name='slug' value={this.getName} />
                  <input
                    type='hidden'
                    name='players'
                    value={this.playersForForm}
                  />
                  {Object.keys(this.formFields).map(field => {
                    return (
                      <input
                        type='hidden'
                        name={field}
                        value={
                          this[
                            `get${field.charAt(0).toUpperCase() +
                              field.slice(1)}`
                          ]
                        }
                      />
                    )
                  })}

                  <button class='btn-Primary' type='submit'>
                    Save
                  </button>
                </form>
              </div>
            </div>

            <div class='bld-Builder_Column'>
              <div class='bld-Builder_Stats'>
                <div class='bld-Stats'>
                  <ul class='bld-Stats_Items'>
                    {map(this.stats, stat => {
                      return (
                        <li class='bld-Stats_Item' style={stat.style}>
                          <span class='bld-Stats_Label'>{stat.label}</span>
                          <span class='bld-Stats_Value'>{stat.value}</span>
                        </li>
                      )
                    })}
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </footer>
      </div>
    )
  }
}
