export class Player {
  constructor ({ index, el }) {
    const _this = this

    this.index = index
    this.els = {
      el,
      pedestal: el.querySelector('.bld-Builder_Pedestal')
    }

    this.object = {}
    this.positions = {
      _fromFormation: '',
      get fromFormation () {
        return this._fromFormation
      },
      set fromFormation (val) {
        this._fromFormation = val
      },

      _inBuilder: '',
      get inBuilder () {
        return this._inBuilder
      },
      set inBuilder (val) {
        this._inBuilder = val

        _this.els.pedestal.innerText = this._inBuilder
      },

      _verbose: '',
      get verbose () {
        return this._verbose
      },
      set verbose (val) {
        this._verbose = val

        _this.els.el.className = `bld-Builder_PlayersItem bld-Builder_PlayersItem-${this._verbose.toLowerCase()}`
      }
    }
  }

  setPosition (key, position) {
    this.positions[key] = position
  }
}
