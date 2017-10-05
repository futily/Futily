import axios from 'axios'
import { Draggable } from '@shopify/draggable'

import formationData from './formationData'
import Search from './Search'
import { Player } from './Player'
import { POSITION_LINES } from './constants'

export class Builder {
  constructor ({ className }) {
    const el = document.querySelector(`.${className}`)

    this.className = className

    this.els = {
      el,
      team: {
        el: el.querySelector(`.${className}_Team`),
        canvas: el.querySelector(`.${className}_Canvas`),
        players: el.querySelector(`.${className}_Players`),
        items: el.querySelectorAll(`.${className}_PlayersItem`)
      },
      form: {
        formation: el.querySelector(`.${className} [name='formation']`),
        name: el.querySelector(`.${className} [name='name']`)
      },
      search: {
        el: el.querySelector('.bld-Search'),
        input: el.querySelector('.bld-Search_Input')
      }
    }

    this.players = {
      team: Array.from(this.els.team.items).map((el, index) => {
        return new Player({ index, el })
      })
    }
    this.search = new Search({ el })

    this.stats = {
      chemistry: {
        el: this.els.el.querySelector(
          `.bld-Stats_Item[data-builder-stat-name='chemistry'] .bld-Stats_Value`
        ),
        input: this.els.el.querySelector(
          `.bld-Stats_Item[data-builder-stat-name='chemistry'] input`
        ),
        _value: 0,
        get value () {
          return this._value
        },
        set value (val) {
          this._value = Number(val)

          this.el.innerText = val
          this.input.value = val
        }
      },
      rating: {
        el: this.els.el.querySelector(
          `.bld-Stats_Item[data-builder-stat-name='rating'] .bld-Stats_Value`
        ),
        input: this.els.el.querySelector(
          `.bld-Stats_Item[data-builder-stat-name='rating'] input`
        ),
        _value: 0,
        get value () {
          return this._value
        },
        set value (val) {
          this._value = Number(val)

          this.el.innerText = val
          this.input.value = val
        }
      },
      attack: {
        el: this.els.el.querySelector(
          `.bld-Stats_Item[data-builder-stat-name='attack'] .bld-Stats_Value`
        ),
        input: this.els.el.querySelector(
          `.bld-Stats_Item[data-builder-stat-name='attack'] input`
        ),
        _value: 0,
        get value () {
          return this._value
        },
        set value (val) {
          this._value = Number(val)

          this.el.innerText = val
          this.input.value = val
        }
      },
      midfield: {
        el: this.els.el.querySelector(
          `.bld-Stats_Item[data-builder-stat-name='midfield'] .bld-Stats_Value`
        ),
        input: this.els.el.querySelector(
          `.bld-Stats_Item[data-builder-stat-name='midfield'] input`
        ),
        _value: 0,
        get value () {
          return this._value
        },
        set value (val) {
          this._value = Number(val)

          this.el.innerText = val
          this.input.value = val
        }
      },
      defence: {
        el: this.els.el.querySelector(
          `.bld-Stats_Item[data-builder-stat-name='defence'] .bld-Stats_Value`
        ),
        input: this.els.el.querySelector(
          `.bld-Stats_Item[data-builder-stat-name='defence'] input`
        ),
        _value: 0,
        get value () {
          return this._value
        },
        set value (val) {
          this._value = Number(val)

          this.el.innerText = val
          this.input.value = val
        }
      },
      pace: {
        el: this.els.el.querySelector(
          `.bld-Stats_Item[data-builder-stat-name='pace'] .bld-Stats_Value`
        ),
        input: this.els.el.querySelector(
          `.bld-Stats_Item[data-builder-stat-name='pace'] input`
        ),
        _value: 0,
        get value () {
          return this._value
        },
        set value (val) {
          this._value = Number(val)

          this.el.innerText = val
          this.input.value = val
        }
      },
      shooting: {
        el: this.els.el.querySelector(
          `.bld-Stats_Item[data-builder-stat-name='shooting'] .bld-Stats_Value`
        ),
        input: this.els.el.querySelector(
          `.bld-Stats_Item[data-builder-stat-name='shooting'] input`
        ),
        _value: 0,
        get value () {
          return this._value
        },
        set value (val) {
          this._value = Number(val)

          this.el.innerText = val
          this.input.value = val
        }
      },
      passing: {
        el: this.els.el.querySelector(
          `.bld-Stats_Item[data-builder-stat-name='passing'] .bld-Stats_Value`
        ),
        input: this.els.el.querySelector(
          `.bld-Stats_Item[data-builder-stat-name='passing'] input`
        ),
        _value: 0,
        get value () {
          return this._value
        },
        set value (val) {
          this._value = Number(val)

          this.input.value = val
          this.el.innerText = val
        }
      },
      dribbling: {
        el: this.els.el.querySelector(
          `.bld-Stats_Item[data-builder-stat-name='dribbling'] .bld-Stats_Value`
        ),
        input: this.els.el.querySelector(
          `.bld-Stats_Item[data-builder-stat-name='dribbling'] input`
        ),
        _value: 0,
        get value () {
          return this._value
        },
        set value (val) {
          this._value = Number(val)

          this.el.innerText = val
          this.input.value = val
        }
      },
      defending: {
        el: this.els.el.querySelector(
          `.bld-Stats_Item[data-builder-stat-name='defending'] .bld-Stats_Value`
        ),
        input: this.els.el.querySelector(
          `.bld-Stats_Item[data-builder-stat-name='defending'] input`
        ),
        _value: 0,
        get value () {
          return this._value
        },
        set value (val) {
          this._value = Number(val)

          this.el.innerText = val
          this.input.value = val
        }
      },
      physical: {
        el: this.els.el.querySelector(
          `.bld-Stats_Item[data-builder-stat-name='physical'] .bld-Stats_Value`
        ),
        input: this.els.el.querySelector(
          `.bld-Stats_Item[data-builder-stat-name='physical'] input`
        ),
        _value: 0,
        get value () {
          return this._value
        },
        set value (val) {
          this._value = Number(val)

          this.el.innerText = val
          this.input.value = val
        }
      }
    }

    this.formation = '442'

    this.setupListeners()

    this.drag = {
      overIndex: null,
      startIndex: null
    }

    this.handleDragStop = this.handleDragStop.bind(this)
    this.handleDragMove = this.handleDragMove.bind(this)
    this.handleDragStart = this.handleDragStart.bind(this)
    new Draggable(document.querySelectorAll('.bld-Builder_Players'), {
      draggable: `.bld-Builder_PlayersItem[data-builder-filled='true']`
    })
      .on('drag:start', this.handleDragStart)
      .on('drag:move', this.handleDragMove)
      .on('drag:stop', this.handleDragStop)

    console.log(this)
  }

  setupListeners () {
    this.els.el.addEventListener('submit', async e => {
      e.preventDefault()

      const data = new FormData(this.els.el)

      const res = await axios({
        data,
        method: 'POST',
        url: this.els.el.action,
        xsrfCookieName: 'csrftoken',
        xsrfHeaderName: 'X-CSRFToken'
      })

      console.log(res)
    })

    this.els.form.formation.addEventListener('change', e => {
      const { target } = e

      this.formation = target.options[target.selectedIndex].value
    })

    this.els.team.el.addEventListener('pointerdown', e => {
      const wantedTarget = e.target.closest('.bld-Builder_PlayersItem')
      if (!wantedTarget) return

      const index = wantedTarget.dataset.builderFormationIndex
      if (this.players.team[index].isFilled()) return

      this.search.startSearch(index)
    })

    this.insertPlayer = this.insertPlayer.bind(this)
    this.els.el.addEventListener('player:selected', evt => {
      const { data, element } = evt.detail
      const index = Number(evt.detail.index)

      this.insertPlayer({ data, element, index })
    })
    this.removePlayer = this.removePlayer.bind(this)
    this.els.el.addEventListener('player:removed', evt => {
      const index = Number(evt.detail.index)

      this.removePlayer({ index })
    })
  }

  handleDragStart (evt) {
    this.drag.startIndex = Array.from(this.els.team.items).indexOf(evt.source)
  }

  handleDragMove (evt) {
    // DragMoveEvent => data => sensorEvent => target
    // If the target is a PlayersItem, set that index to be read on DragStopEvent
    // If the target is no longer a PlayersItem don't set an index
    // Voila?
    const target = evt.sensorEvent.target.closest('.bld-Builder_PlayersItem')

    this.drag.overIndex = Array.from(this.els.team.items).includes(target)
      ? Array.from(this.els.team.items).indexOf(target)
      : null
  }

  handleDragStop () {
    if (
      this.drag.overIndex !== null &&
      this.drag.overIndex !== this.drag.startIndex
    ) {
      const sourcePlayer = this.players.team[this.drag.startIndex]
      const sourceObj = {
        data: JSON.parse(JSON.stringify(sourcePlayer.data)),
        element: sourcePlayer.cloneCard(),
        index: this.drag.startIndex
      }

      const targetPlayer = this.players.team[this.drag.overIndex]
      const targetObj = targetPlayer.isFilled()
        ? {
          data: JSON.parse(JSON.stringify(targetPlayer.data)),
          element: targetPlayer.cloneCard(),
          index: this.drag.overIndex
        }
        : {
          data: null,
          element: null,
          index: this.drag.overIndex
        }

      if (targetPlayer.isFilled()) {
        this.removePlayer({ index: sourceObj.index })
        this.removePlayer({ index: targetObj.index })

        this.insertPlayer({
          data: sourceObj.data,
          element: sourceObj.element,
          index: targetObj.index
        })
        this.insertPlayer({
          data: targetObj.data,
          element: targetObj.element,
          index: sourceObj.index
        })

        this.drag.startIndex = null
        this.drag.overIndex = null
      } else {
        this.insertPlayer({
          data: sourceObj.data,
          element: sourceObj.element,
          index: targetObj.index
        })
        this.removePlayer({ index: this.drag.startIndex })
      }
    }
  }

  getAverageLine (line) {
    if (!['DEF', 'MID', 'ATT'].includes(line)) {
      throw new Error('"line" must be "DEF", "MID" or "ATT"')
    }

    const players = this.players.team.filter(
      player =>
        player.isFilled() &&
        POSITION_LINES[line].includes(player.positions.fromFormation)
    )

    return this.getAverageStat({
      players,
      stat: 'rating',
      includeGk: line === 'DEF'
    })
  }

  getAverageStat ({ players, stat, includeGk = false }) {
    // We might not want the goalkeeper when calculating things like 'pace'
    if (!includeGk) {
      players = players.filter(
        player => player.index !== 0 && player.isFilled()
      )
    }

    return Math.round(
      players.reduce((acc, player) => {
        acc += player.isFilled() ? player.data[stat] : 0

        return acc
      }, 0) / players.length || 0
    )
  }

  updateStats () {
    const players = this.players.team

    this.stats.rating.value = this.getAverageStat({ players, stat: 'rating' })
    this.stats.chemistry.value = Math.min(
      Math.max(
        0,
        players.reduce((acc, player) => {
          acc += player.chemistry.total

          return acc
        }, 0)
      ),
      100
    )

    this.stats.attack.value = this.getAverageLine('ATT')
    this.stats.midfield.value = this.getAverageLine('MID')
    this.stats.defence.value = this.getAverageLine('DEF')

    this.stats.pace.value = this.getAverageStat({ players, stat: 'card_att_1' })
    this.stats.shooting.value = this.getAverageStat({
      players,
      stat: 'card_att_2'
    })
    this.stats.passing.value = this.getAverageStat({
      players,
      stat: 'card_att_3'
    })
    this.stats.dribbling.value = this.getAverageStat({
      players,
      stat: 'card_att_4'
    })
    this.stats.defending.value = this.getAverageStat({
      players,
      stat: 'card_att_5'
    })
    this.stats.physical.value = this.getAverageStat({
      players,
      stat: 'card_att_6'
    })
  }

  clearCanvas () {
    const canvas = this.els.team.canvas
    canvas.width = this.els.team.canvas.offsetWidth
    canvas.height = this.els.team.canvas.offsetHeight
    canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height)
  }

  initCanvas () {
    this.clearCanvas()

    this.chemLinks.map(link => {
      const player = this.players.team[link.a]
      const target = this.players.team[link.b]

      this.drawLine(
        player.getCoordinates(),
        target.getCoordinates(),
        player.calculateIndividualLinkChemistry(target)
      )
    })
  }

  drawLine (start, end, chemistry) {
    const context = this.els.team.canvas.getContext('2d')
    const color =
      chemistry >= 2 ? '#a5f35c' : chemistry >= 1 ? '#cf8600' : '#a31a19'
    context.lineWidth = 3
    context.strokeStyle = color
    context.lineCap = 'round'
    context.shadowOffsetY = 1.5
    context.shadowColor = 'rgba(0, 0, 0, 0.5)'
    context.shadowBlur = 1.5
    context.beginPath()
    context.moveTo(start.x, start.y)
    context.lineTo(end.x, end.y)
    context.stroke()
  }

  insertPlayer ({ data, element, index }) {
    const teamPlayer = this.players.team[index]
    teamPlayer.constructPlayer({ data, element })

    this.players.team.map(player => {
      if (player.links.includes(index)) player.filledLinks.push(index)
    })

    this.updateChemistry()
    this.updateStats()
  }

  removePlayer ({ index }) {
    const player = this.players.team[index]
    player.removePlayer()

    this.players.team.map(player => {
      if (player.links.includes(index)) {
        player.filledLinks = [
          ...player.filledLinks.filter(link => link !== index)
        ]
      }
    })

    this.updateChemistry()
  }

  updateChemistry () {
    this.players.team.filter(player => player.isFilled()).map(player => {
      player.calculateLinkChemistry(this.players.team)
      player.calculatePositionChemistry()
    })

    this.initCanvas()
  }

  get formation () {
    return this._formation
  }

  set formation (val) {
    this._formation = val

    this.players.team.map((player, index) => {
      player.setPosition(
        'fromFormation',
        formationData[this._formation]['positions'][index]
      )
      player.setPosition(
        'verbose',
        formationData[this._formation]['verbose'][index]
      )
      player.setLinks({ formation: this._formation, team: this.players.team })

      if (player.isFilled()) {
        player.setInBuilderPosition()
      }
    })

    this.chemLinks = formationData[this._formation].chemLinkData

    this.els.el.setAttribute('data-builder-formation', this._formation)

    this.updateChemistry()
  }
}
