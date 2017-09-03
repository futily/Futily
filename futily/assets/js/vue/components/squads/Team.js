import Vue from 'vue'
import Component from 'vue-class-component'
import { mapActions, mapGetters, mapMutations } from 'vuex'
import { cloneDeep, debounce, isEmpty, map } from 'lodash'

import { Player } from './Player'
import * as types from './types'
import { playerToPlayerChemistry } from './module'
import { Card } from '../players/Card'

const baseSearch = {
  count: 0,
  pagination: {
    next: null,
    prev: null
  },
  pages: {
    current: 1,
    total: 1
  },
  results: []
}

@Component({
  components: {
    Card,
    Player
  },

  props: {
    isTransitioning: {
      type: Boolean
    }
  },

  computed: {
    ...mapGetters({
      getPlayer: types.GET_PLAYER,
      getPlayers: types.GET_PLAYERS,
      getPlayerFormationLinks: types.GET_PLAYER_FORMATION_LINKS,
      getPlayerChemistry: types.GET_PLAYER_CHEMISTRY,
      getSearch: types.GET_SEARCH
    })
  },

  watch: {
    isTransitioning (val) {
      // if (val) return
      // setTimeout(() => {
      //   this.initCanvas()
      // })
    },

    'getSearch.open' (val) {
      if (val) this.$nextTick(() => this.$refs.searchInput.focus())
    }
  },

  methods: {
    ...mapActions({
      setPlayer: types.SET_PLAYER
    }),

    ...mapMutations({
      setSearch: types.SET_SEARCH
    })
  }
})
export class Team extends Vue {
  search = cloneDeep(baseSearch)
  searchLoading = false
  searchTerm = ''

  // mounted () {
  //   setTimeout(() => {
  //     this.initCanvas()
  //   }, 500)
  // }

  initCanvas () {
    const canvas = this.$refs.canvas
    canvas.setAttribute('width', `${canvas.offsetWidth}`)
    canvas.setAttribute('height', `${canvas.offsetHeight}`)
    const ctx = canvas.getContext('2d')
    ctx.clearRect(0, 0, canvas.offsetWidth, canvas.offsetHeight)
    const teamPlayers = this.getPlayers.team

    map(this.$refs.players, (el, index) => {
      const links = this.getPlayerFormationLinks(index)
      const { x: moveX, y: moveY } = getMoveCoords(el)

      map(links, link => {
        const linkedEl = this.$refs.players[link]
        const { x: lineX, y: lineY } = getMoveCoords(linkedEl)
        const colour = {
          3.5: '#54a71b',
          3: '#90c030',
          2: '#d47c00',
          0.9: '#bf3030'
        }[playerToPlayerChemistry(teamPlayers[index], teamPlayers[link])]

        ctx.beginPath()
        ctx.moveTo(moveX, moveY)
        ctx.lineTo(lineX, lineY)
        ctx.closePath()
        ctx.lineWidth = 7
        ctx.strokeStyle = '#5a5a5a'
        ctx.stroke()

        ctx.beginPath()
        ctx.moveTo(moveX, moveY)
        ctx.lineTo(lineX, lineY)
        ctx.closePath()
        ctx.lineWidth = 5
        ctx.strokeStyle = colour
        ctx.stroke()
      })
    })

    // This runs after so we can ensure the diamond is on top
    map(this.$refs.players, (el, index) => {
      const chemistry = this.getPlayerChemistry({ index })
      const colour = {
        10: '#54a71b',
        9: '#54a71b',
        8: '#90c030',
        7: '#90c030',
        6: '#90c030',
        5: '#d47c00',
        4: '#d47c00',
        3: '#d47c00',
        2: '#d47c00',
        1: '#bf3030'
      }[chemistry]
      const { x: moveX, y: moveY } = getMoveCoords(el)

      ctx.beginPath()
      const numberOfSides = 6
      const size = 12
      const Xcenter = moveX
      const Ycenter = moveY
      ctx.moveTo(
        Xcenter + (size + 10) * Math.cos(0),
        Ycenter + size * Math.sin(0)
      )

      for (let i = 1; i <= numberOfSides; i += 1) {
        ctx.lineTo(
          Xcenter + (size + 10) * Math.cos(i * 2 * Math.PI / numberOfSides),
          Ycenter + size * Math.sin(i * 2 * Math.PI / numberOfSides)
        )
      }
      ctx.fillStyle = colour
      ctx.fill()
      ctx.lineWidth = 1
      ctx.strokeStyle = '#5a5a5a'
      ctx.stroke()
    })

    function getMoveCoords (el) {
      const elStyle = window.getComputedStyle(el)
      const elX = parseInt(elStyle.getPropertyValue('--PlayerX'), 10)
      const elY = parseInt(elStyle.getPropertyValue('--PlayerY'), 10)

      return {
        x: el.offsetLeft - elX,
        y: el.offsetTop - elY + (el.offsetHeight / 2 - 7)
      }
    }
  }

  handleSearch ($evt) {
    const wantedTarget = $evt.target.closest('.bld-Builder_PlayersItem')
    const index = this.$refs.players.indexOf(wantedTarget)

    if (!isEmpty(this.getPlayer({ index }).player)) return

    this.setSearch({ open: true, position: index, term: '' })
  }

  async handleSearchInput (e) {
    const { value } = e.target
    this.sync('searchTerm', value)

    if (value.length > 2) {
      const res = await this.$http.get(
        `/api/players?query=${this.searchTerm}&page=${this.search.pages
          .current}`
      )
      const { data } = res

      this.setSearchData(data)
    }
  }

  async handleSearchResultsPrev ($evt) {
    $evt.stopPropagation()

    this.searchLoading = true
    const res = await this.$http.get(
      `/api/players?query=${this.searchTerm}&page=${this.search.pagination
        .prev}`
    )
    this.searchLoading = false
    const { data } = res

    this.setSearchData(data)
  }

  async handleSearchResultsNext ($evt) {
    $evt.stopPropagation()

    this.searchLoading = true
    const res = await this.$http.get(
      `/api/players?query=${this.searchTerm}&page=${this.search.pagination
        .next}`
    )
    this.searchLoading = false
    const { data } = res

    this.setSearchData(data)
  }

  handleSearchResultsClick ($event, player) {
    this.setPlayer({ group: 'team', index: this.getSearch.position, player })
    this.$refs.searchInput.value = ''
    this.searchTerm = ''
    this.setSearch({ open: false })

    this.search = cloneDeep(baseSearch)
    // this.initCanvas()
  }

  setSearchData (data) {
    this.search = {
      count: data.count,
      results: data.results,
      pages: data.pages,
      pagination: {
        next: data.links.next ? data.pages.current + 1 : null,
        prev: data.links.previous ? data.pages.current - 0 : null
      }
    }
  }

  sync (prop, value) {
    this[prop] = value
  }

  render () {
    /* eslint-disable indent */
    return (
      <div class='bld-Builder_Team'>
        <canvas class='bld-Builder_Canvas' ref='canvas' />

        <ul class='bld-Builder_Players'>
          {Object.keys(this.getPlayers.team).map((playerKey, index) => {
            const player = this.getPlayers.team[playerKey]

            return (
              <li
                class={[
                  'bld-Builder_PlayersItem',
                  `bld-Builder_PlayersItem-${player.positions.formationActual.toLowerCase()}`
                ]}
                ref='players'
                refInFor
                onClick={this.handleSearch}
              >
                <Player index={index} player={player} />
              </li>
            )
          })}
        </ul>

        <transition name='trn-Fade'>
          <div
            class='bld-Search'
            v-show={this.getSearch.open}
            onClick={e => this.setSearch({ open: false })}
          >
            <header class='bld-Search_Header'>
              <input
                class='bld-Search_Input'
                type='search'
                placeholder='Search'
                onInput={debounce(this.handleSearchInput, 300)}
                ref='searchInput'
              />
            </header>

            <div class='bld-Search_Body'>
              <div
                class={{
                  'bld-Search_Results': true,
                  'bld-Search_Results-loading': this.searchLoading
                }}
              >
                {this.search.pagination.prev
                  ? <button
                      rel='prev'
                      class='bld-Search_Prev'
                      onClick={e => this.handleSearchResultsPrev(e)}
                    >
                      <svg
                        xmlns='http://www.w3.org/2000/svg'
                        viewBox='0 0 129 129'
                      >
                        <path d='M88.6 121.3c.8.8 1.8 1.2 2.9 1.2s2.1-.4 2.9-1.2c1.6-1.6 1.6-4.2 0-5.8l-51-51 51-51c1.6-1.6 1.6-4.2 0-5.8s-4.2-1.6-5.8 0l-54 53.9c-1.6 1.6-1.6 4.2 0 5.8l54 53.9z' />
                      </svg>
                    </button>
                  : ''}

                <div class='bld-Search_Items'>
                  <ul
                    class='plyr-CardList_Items'
                    v-show={this.search.results.length > 0}
                  >
                    {this.search.results.map(player => {
                      return (
                        <li
                          class='plyr-CardList_Item'
                          onClick={e =>
                            this.handleSearchResultsClick(e, player)}
                        >
                          <Card player={player} />
                        </li>
                      )
                    })}
                  </ul>
                </div>

                {this.search.pagination.next
                  ? <button
                      rel='next'
                      class='bld-Search_Next'
                      onClick={e => this.handleSearchResultsNext(e)}
                    >
                      <svg
                        xmlns='http://www.w3.org/2000/svg'
                        viewBox='0 0 129 129'
                      >
                        <path d='M40.4 121.3c-.8.8-1.8 1.2-2.9 1.2s-2.1-.4-2.9-1.2c-1.6-1.6-1.6-4.2 0-5.8l51-51-51-51c-1.6-1.6-1.6-4.2 0-5.8 1.6-1.6 4.2-1.6 5.8 0l53.9 53.9c1.6 1.6 1.6 4.2 0 5.8l-53.9 53.9z' />
                      </svg>
                    </button>
                  : ''}
              </div>
            </div>
          </div>
        </transition>
      </div>
    )
  }
}
