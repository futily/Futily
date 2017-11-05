import { EditablePlayer, Player } from './Player'
import formationData from './formationData'

export class Squad {
  constructor ({ className, isEditable = false }) {
    const el = document.querySelector(`.${className}`)

    this.className = className
    this.isEditable = isEditable

    this.els = {
      el,
      team: {
        el: el.querySelector(`.${className}_Team`),
        canvas: el.querySelector(`.${className}_Canvas`),
        players: el.querySelector(`.${className}_Players`),
        items: el.querySelectorAll(`.${className}_PlayersItem`)
      }
    }

    this.players = {
      team: Array.from(this.els.team.items).map((el, index) => {
        const playerEl = el.querySelector('.bld-Builder_Player')
        const initialData = playerEl.dataset['builderInitialData']
          ? JSON.parse(playerEl.dataset['builderInitialData'])
          : {}
        const initialCard = playerEl.querySelector('.plyr-Card')
        const PlayerClass = this.isEditable ? EditablePlayer : Player
        const player = new PlayerClass({
          index,
          el,
          initialData,
          initialCard,
          isEditable: this.isEditable
        })
        if (player.isFilled) {
          player.setPosition(player.els.pedestal.innerText)
        }

        return player
      })
    }
    this.initialFormation = this.els.el.dataset['builderFormation']

    this.chemLinks = formationData[this.initialFormation].chemLinkData

    this.formation = this.initialFormation
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

  updateChemistry () {
    this.players.team.filter(player => player.isFilled).map(player => {
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

      if (player.isFilled && this.isEditable) {
        player.setInBuilderPosition()
      }
    })

    this.chemLinks = formationData[this._formation].chemLinkData

    this.els.el.setAttribute('data-builder-formation', this._formation)

    this.updateChemistry()
  }
}
