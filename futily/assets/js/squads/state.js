const state = {
  subscriptions: {},

  data: {
    _formation: '442',
    get formation () {
      return this._formation
    },

    set formation (val) {
      this._formation = val

      if (
        state.subscriptions.hasOwnProperty('formation') &&
        state.subscriptions.formation.listeners.length
      ) {
        state.subscriptions.formation.listeners.map(fnc =>
          fnc({ formation: this._formation })
        )
      }
    }
  },

  subscribe (key, fnc) {
    if (Object.keys(this.data).includes(key) === false) {
      throw new Error(`Key: ${key} does not exist in the state`)
    }

    if (this.subscriptions.hasOwnProperty(key) === false) {
      this.subscriptions[key] = {
        listeners: []
      }
    }

    if (
      this.subscriptions.hasOwnProperty(key) &&
      this.subscriptions[key].hasOwnProperty('listeners')
    ) {
      this.subscriptions[key].listeners.push(fnc)
    }
  }
}

export default state

// Set a state tree
// Able to subscribe to keys of state
// Update all references to state
