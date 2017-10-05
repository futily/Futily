import { cloneDeep, isEmpty } from 'lodash'

import * as types from './types'
import positionMap from './utils/positionMap'
import { goodChem, weakChem } from './utils/chemPosition'
import positionLinks from './utils/positionLinks'
import { POSITION_LINES } from './utils/constants'
import allowedPositions from './utils/allowedPositions'

const playerObj = {
  player: {},
  chemistry: {
    links: 0,
    position: 0,
    boost: 0
  },
  positions: {
    formation: '',
    formationActual: '',
    actual: ''
  },
  links: {
    formation: [],
    filled: []
  }
}

const state = {
  name: '',
  formation: '442',
  search: {
    open: false,
    position: undefined
  },
  filledLinks: [],

  chemistry: 0,
  rating: 0,

  attack: 0,
  midfield: 0,
  defence: 0,

  pace: 0,
  shooting: 0,
  passing: 0,
  dribbling: 0,
  defending: 0,
  physical: 0,

  team: {
    0: cloneDeep(playerObj),
    1: cloneDeep(playerObj),
    2: cloneDeep(playerObj),
    3: cloneDeep(playerObj),
    4: cloneDeep(playerObj),
    5: cloneDeep(playerObj),
    6: cloneDeep(playerObj),
    7: cloneDeep(playerObj),
    8: cloneDeep(playerObj),
    9: cloneDeep(playerObj),
    10: cloneDeep(playerObj)
  },

  bench: {
    11: cloneDeep(playerObj),
    12: cloneDeep(playerObj),
    13: cloneDeep(playerObj),
    14: cloneDeep(playerObj),
    15: cloneDeep(playerObj),
    16: cloneDeep(playerObj),
    17: cloneDeep(playerObj)
  },

  reserve: {
    18: cloneDeep(playerObj),
    19: cloneDeep(playerObj),
    20: cloneDeep(playerObj),
    21: cloneDeep(playerObj),
    22: cloneDeep(playerObj)
  }
}

const mutations = {
  [types.SET_FORMATION] (state, { formation }) {
    state.formation = formation
  },

  [types.SET_FORMATION_POSITIONS] (state, { formation }) {
    const positions = positionMap[formation]

    Object.keys(positions.positions).map(index => {
      state.team[index].positions.formation = positions['positions'][index]
      state.team[index].positions.formationActual = positions['verbose'][index]
    })
  },

  [types.SET_FORMATION_LINKS] (state, { formation }) {
    const links = positionLinks[formation]

    Object.keys(links).map(index => {
      state.team[index].links.formation = links[index]
    })
  },

  [types.SET_PLAYER_CHEMISTRY] (state, { group, index }) {
    const statePlayer = state[group][index]

    if (Object.keys(statePlayer.player).length !== 0) {
      const linkChem = calculateLinkChemistry(state, statePlayer)
      const positionChem = calculatePositionChemistry(statePlayer)

      statePlayer.chemistry.links = linkChem
      statePlayer.chemistry.position = positionChem
    } else {
      statePlayer.chemistry.links = 0
      statePlayer.chemistry.position = 0
    }
  },

  [types.SET_PLAYER_FILLED_LINKS] (state, { group, index }) {
    const statePlayer = state[group][index]

    statePlayer.links.formation.map(linkedIndex => {
      const player = state[group][linkedIndex]

      player.links.filled.push(index)
    })
  },

  [types.SET_PLAYER_OBJECT] (state, { group, index, player, position }) {
    const statePlayer = state[group][index]

    if (position == null) {
      const formationPosition = state[group][index].positions.formation
      const playerPosition = player.position

      position = allowedPositions[formationPosition].includes(playerPosition)
        ? formationPosition
        : playerPosition
    }

    statePlayer.player = player
    statePlayer.positions.actual = position

    if (isTeam(index)) {
      state.Links.push(index)
    }
  },

  [types.SET_NAME] (state, { name }) {
    state.name = name
  },

  [types.SET_SEARCH] (state, { open, position }) {
    Object.assign(state.search, { open, position })
  },

  [types.REMOVE_PLAYER_OBJECT] (state, { group, index }) {
    const statePlayer = state[group][index]
    statePlayer.player = {}

    if (isTeam(index)) {
      state.Links = state.Links.filter(item => item !== index)
    }
  },

  [types.REMOVE_PLAYER_FILLED_LINKS] (state, { group, index }) {
    const statePlayer = state[group][index]

    statePlayer.links.formation.map(linkedIndex => {
      const player = state[group][linkedIndex]

      player.links.filled = player.links.filled.filter(item => item !== index)
    })
  }
}

const actions = {
  [types.SET_FORMATION] ({ commit, state }, { formation }) {
    commit(types.SET_FORMATION, { formation })
    commit(types.SET_FORMATION_POSITIONS, { formation })
    commit(types.SET_FORMATION_LINKS, { formation })

    // Update player chemistry after formation change
    state.Links.map(filledIndex => {
      const group = 'team'
      const player = state[group][filledIndex].player

      commit(types.SET_PLAYER_OBJECT, { group, index: filledIndex, player })
      commit(types.SET_PLAYER_CHEMISTRY, { group, index: filledIndex, player })
    })
  },

  [types.SET_PLAYER] (
    { commit, state },
    { group, index, player, position = null }
  ) {
    const payload = { group, index, player, position }

    // Set the API object to the formations "player"
    commit(types.SET_PLAYER_OBJECT, payload)
    // Fill our current indexes links.formation with itself
    commit(types.SET_PLAYER_FILLED_LINKS, payload)
    // Calculate our chemistry
    commit(types.SET_PLAYER_CHEMISTRY, payload)

    // Since we've added a new player to the builder, chances are there are players linked to it that need their chemistry recalculated
    const filledLinks = state[group][index].links.filled
    filledLinks.map(filledIndex => {
      commit(types.SET_PLAYER_CHEMISTRY, {
        group,
        index: filledIndex,
        player: state[group][filledIndex].player
      })
    })
  },

  [types.REMOVE_PLAYER] ({ commit, state }, { group, index }) {
    commit(types.REMOVE_PLAYER_OBJECT, { group, index })
    commit(types.REMOVE_PLAYER_FILLED_LINKS, { group, index })
    commit(types.SET_PLAYER_CHEMISTRY, { group, index, player: {} })

    const filledLinks = state[group][index].links.filled
    filledLinks.map(filledIndex => {
      commit(types.SET_PLAYER_CHEMISTRY, {
        group,
        index: filledIndex,
        player: state[group][filledIndex].player
      })
    })
  }
}

const getters = {
  [types.GET_PLAYERS] (state) {
    const { team, bench, reserve } = state

    return { team, bench, reserve }
  },

  [types.GET_PLAYER]: state => ({ group = 'team', index }) => {
    return state[group][index]
  },

  [types.GET_PLAYER_CHEMISTRY]: state => ({ group = 'team', index }) => {
    const player = state[group][index]
    const roundedChem = Math.round(
      player.chemistry.links * player.chemistry.position
    )

    return Math.min(10, roundedChem + player.chemistry.boost)
  },

  [types.GET_PLAYER_FORMATION_LINKS]: state => index => {
    return state.team[index].links.formation
  },

  [types.GET_CHEMISTRY] (_, getters) {
    return Math.max(
      0,
      state.Links.reduce(
        (acc, val) => acc + getters[types.GET_PLAYER_CHEMISTRY]({ index: val }),
        0
      )
    )
  },

  [types.GET_PLAYER_OBJECT_IDS] (state) {
    return state.Links.map(index => {
      return state.team[index].player.id
    })
  },

  [types.PLAYERS_FOR_FORM] (state) {
    return state.Links
      .map(index => {
        const player = state.team[index]

        return `${player.player.id},${index},${player.positions.actual}`
      })
      .join('|')
  },

  [types.GET_RATING]: state => getAverageStat(state, state.Links, 'rating'),

  [types.GET_ATTACK]: state => getAverageLine(state, 'ATT'),
  [types.GET_MIDFIELD]: state => getAverageLine(state, 'MID'),
  [types.GET_DEFENCE]: state => getAverageLine(state, 'DEF'),

  [types.GET_PACE]: state =>
    getAverageStat(state, state.Links, 'card_att_1', false),
  [types.GET_SHOOTING]: state =>
    getAverageStat(state, state.Links, 'card_att_2', false),
  [types.GET_PASSING]: state =>
    getAverageStat(state, state.Links, 'card_att_3', false),
  [types.GET_DRIBBLING]: state =>
    getAverageStat(state, state.Links, 'card_att_4', false),
  [types.GET_DEFENDING]: state =>
    getAverageStat(state, state.Links, 'card_att_5', false),
  [types.GET_PHYSICAL]: state =>
    getAverageStat(state, state.Links, 'card_att_6', false),

  [types.GET_SEARCH]: state => state.search,
  [types.GET_FORMATION]: state => state.formation,
  [types.GET_NAME]: state => state.name
}

export default {
  state,
  mutations,
  actions,
  getters
}

function getAverageLine (state, line) {
  if (!['DEF', 'MID', 'ATT'].includes(line)) {
    throw new Error('"line" must be "DEF", "MID" or "ATT"')
  }

  const players = state.Links.filter(index => {
    const position = state.team[index].positions.formation

    return POSITION_LINES[line].includes(position)
  })

  return getAverageStat(state, players, 'rating')
}

function getAverageStat (state, players, stat, includeGk = false) {
  // We might not want the goalkeeper when calculating things like 'pace'
  if (!includeGk) players = players.filter(index => index !== 0)

  return Math.round(
    players.reduce((acc, val) => acc + state.team[val].player[stat], 0) /
      players.length || 0
  )
}

function calculatePositionChemistry (player) {
  const positionChemSchema = {
    strong: 3,
    good: 2.5,
    weak: 1.5,
    poor: 0.5
  }
  const playerPosition = player.positions.actual

  if (playerPosition === player.positions.formation) {
    return positionChemSchema.strong
  } else if (
    goodChem.hasOwnProperty(player.positions.formation) &&
    goodChem[player.positions.formation].includes(playerPosition)
  ) {
    return positionChemSchema.good
  } else if (
    weakChem.hasOwnProperty(player.positions.formation) &&
    weakChem[player.positions.formation].includes(playerPosition)
  ) {
    return positionChemSchema.weak
  } else {
    return positionChemSchema.poor
  }
}

function calculateLinkChemistry (state, player) {
  const playerLinks = player.links.filled
  let chemClub = 0
  let chemLeague = 0
  let chemNation = 0

  for (const index of playerLinks) {
    const linkedPlayer = state.team[index]

    if (player.player.club.title === linkedPlayer.player.club.title) {
      chemClub++
    }

    if (
      player.player.league.title === linkedPlayer.player.league.title ||
      [player.player.league.title, linkedPlayer.player.league.title].includes(
        2118
      )
    ) {
      chemLeague++
    }

    if (player.player.nation.title === linkedPlayer.player.nation.title) {
      chemNation++
    }
  }

  chemClub = playerLinks.length && chemClub / playerLinks.length * 3
  chemLeague = playerLinks.length && chemLeague / playerLinks.length * 3
  chemNation = playerLinks.length && chemNation / playerLinks.length * 3

  const chemTotal = chemClub + chemLeague + chemNation

  if (chemTotal >= 5) {
    return 3.5
  } else if (chemTotal >= 3) {
    return 3
  } else if (chemTotal >= 1) {
    return 2
  } else {
    return 0.9
  }
}

export function playerToPlayerChemistry (player, linkedPlayer) {
  if (isEmpty(player.player) || isEmpty(linkedPlayer.player)) return 0.9

  let chemClub = 0
  let chemLeague = 0
  let chemNation = 0

  if (player.player.club.title === linkedPlayer.player.club.title) {
    chemClub += 2
  }

  if (
    player.player.league.title === linkedPlayer.player.league.title ||
    [player.player.league.title, linkedPlayer.player.league.title].includes(
      2118
    )
  ) {
    chemLeague += 1
  }

  if (player.player.nation.title === linkedPlayer.player.nation.title) {
    chemNation += 1
  }

  const chemTotal = chemClub + chemLeague + chemNation

  if (chemTotal >= 4) {
    return 3.5
  } else if (chemTotal >= 3) {
    return 3
  } else if (chemTotal >= 1) {
    return 2
  } else {
    return 0.9
  }
}

const isTeam = index => index <= 10
