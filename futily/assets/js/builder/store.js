import Vuex from 'vuex';
import clone from 'clone';

import Vue from '../vue';
import { range } from '../utils';
import * as types from './types';
import formationData from './utils/formationData';
import allowedPositions from './utils/allowedPositions';
import { getAverageLine, getAverageStat } from './utils/utils';
import { goodChem, weakChem } from './utils/chemPosition';

Vue.use(Vuex);

const strict = process.env.NODE_ENV !== 'production';

const playerSchema = {
  chemistry: {
    boost: 0,
    links: 0,
    positions: 0,
    total: 0,
  },
  data: {},
  el: null,
  filledLinks: [],
  formationLinks: [],
  index: null,
  positions: {
    fromFormation: '',
    inBuilder: '',
    verbose: '',
  },
  isFilled: false,

  calculateIndividualLinkChemistry (target) {
    if (this.isFilled === false || target.isFilled === false) {
      return 0;
    }

    let chemClub = 0;
    let chemLeague = 0;
    let chemNation = 0;

    if (this.data.club.title === target.data.club.title) {
      chemClub++;
    }

    if (
      this.data.league.title === target.data.league.title ||
      [this.data.league.ea_id, target.data.league.ea_id].includes(2118)
    ) {
      chemLeague++;
    }

    if (this.data.nation.title === target.data.nation.title) {
      chemNation++;
    }

    return chemClub + chemLeague + chemNation;
  },

  getCoordinates () {
    const style = window.getComputedStyle(this.el).transform;
    const match = style.match(/^matrix\((.+)\)$/)[1].split(',');
    const x =
      this.el.offsetLeft + parseFloat(match[4]) + this.el.offsetWidth / 2;
    const y =
      this.el.offsetTop +
      parseFloat(match[5]) +
      (this.el.offsetHeight / 2 + 100);

    return {
      x,
      y,
    };
  },
};

const state = {
  isSbc: false,
  formation: '442',
  isEditable: true,
  sbcId: undefined,
  sbcPassed: false,
  sbcRequirements: [],
  title: '',
  page: null,
  user: {
    id: null,
    username: null,
    link: null,
  },
  share: {
    url: '',
    title: '',
  },

  chemLinks: [],
  players: {
    team: range(11).map(index => {
      const player = clone(playerSchema);
      player.index = index;

      return player;
    }),
    bench: range(7, 11).map(index => {
      const player = clone(playerSchema);
      player.index = index;

      return player;
    }),
    reserves: range(5, 18).map(index => {
      const player = clone(playerSchema);
      player.index = index;

      return player;
    }),
  },

  search: {
    index: null,
    open: false,
    pages: {
      next: null,
      prev: null,
      current: 1,
      total: 1,
    },
    results: [],
    term: '',
  },
};

const mutations = {
  [types.SETUP] (state, { elements: { team }, page }) {
    state.players.team.forEach(player => {
      player.el = team[player.index];
    });
    state.page = page;
  },

  [types.CLOSE_SEARCH] (state) {
    state.search.open = false;
    state.search.index = null;
    state.search.results = [];
    state.search.term = '';
  },

  [types.INSERT_PLAYER] (state, { data, index }) {
    index = index === undefined ? state.search.index : index;
    const player = getPlayer(state, index);
    player.data = data;
    player.positions.inBuilder = player.data.position;
    player.isFilled = true;
  },

  [types.REMOVE_PLAYER] (state, { index }) {
    const player = getPlayer(state, index);
    player.isFilled = false;
    player.data = {};
  },

  [types.OPEN_SEARCH] (state, { index }) {
    state.search.open = true;
    state.search.index = index;
  },

  [types.RESET_SEARCH_PAGES] (state) {
    Object.assign(state.search.pages, {
      next: '',
      prev: '',
      current: 1,
      total: 1,
    });
  },

  [types.SET_CHEMLINKS] (state, { formation }) {
    state.chemLinks = formationData[formation].chemLinkData;
  },

  [types.SET_FORMATION] (state, { formation }) {
    state.formation = formation;
  },

  [types.TOGGLE_PLAYER_BOOST] (state, { index }) {
    const player = getPlayer(state, index);
    player.chemistry.boost = player.chemistry.boost === 0 ? 1 : 0;
    player.chemistry.total = getTotalChem(player);
  },

  [types.SET_PLAYER_POSITION] (state, { index, position }) {
    const player = getPlayer(state, index);
    player.positions.inBuilder = position;
    player.chemistry.positions = calculatePositionChemistry(player);
    player.chemistry.total = getTotalChem(player);
  },

  [types.SET_SBC_REQUIREMENT_PASSED] (state, { index, passed }) {
    state.sbcRequirements[index].passed = passed;
    state.sbcPassed =
      state.sbcRequirements.filter(requirement => requirement.passed).length ===
      state.sbcRequirements.length;
  },

  [types.SET_SEARCH_PAGES] (state, { pages }) {
    Object.assign(state.search.pages, pages);
  },

  [types.SET_SEARCH_RESULTS] (state, { results }) {
    state.search.results = results;
  },

  [types.SET_SEARCH_TERM] (state, { term }) {
    state.search.term = term;
  },

  [types.SET_TITLE] (state, { title }) {
    state.title = title;
  },

  [types.UPDATE_PLAYERS] (state, { formation }) {
    updatePlayers({ formation, players: state.players.team });
  },
};

const actions = {
  [types.SETUP] ({ commit, state }, { elements, page }) {
    commit(types.SETUP, { elements, page });
    commit(types.SET_CHEMLINKS, { formation: state.formation });
    commit(types.UPDATE_PLAYERS, { formation: state.formation });
  },

  [types.INSERT_PLAYER] ({ commit, state }, { data, index }) {
    commit(types.INSERT_PLAYER, { data, index });
    commit(types.UPDATE_PLAYERS, { formation: state.formation });
    commit(types.CLOSE_SEARCH);
  },

  [types.REMOVE_PLAYER] ({ commit, state }, { index }) {
    commit(types.REMOVE_PLAYER, { index });
    commit(types.UPDATE_PLAYERS, { formation: state.formation });
  },

  [types.SET_FORMATION] ({ commit }, { formation }) {
    commit(types.SET_FORMATION, { formation });
    commit(types.SET_CHEMLINKS, { formation });
    commit(types.UPDATE_PLAYERS, { formation });
  },
};

const getters = {
  [types.GET_CHEMLINKS]: state => state.chemLinks,
  [types.GET_FILLED_TEAM_INDEXES]: state =>
    state.players.team.filter(player => player.isFilled),
  [types.GET_FORMATION]: state => state.formation,
  [types.GET_IS_EDITABLE]: state => state.isEditable,
  [types.GET_IS_SBC]: state => state.isSbc,
  [types.GET_TITLE]: state => state.title,
  [types.GET_PAGE]: state => state.page,
  [types.GET_PLAYERS]: state => state.players,
  [types.GET_SBC_AWARDS]: state => state.sbcAwards,
  [types.GET_SBC_ID]: state => state.sbcId,
  [types.GET_SBC_PASSED]: state => state.sbcPassed,
  [types.GET_SBC_REQUIREMENTS]: state => state.sbcRequirements,
  [types.GET_SHARE]: state => state.share,
  [types.GET_SEARCH]: state => state.search,
  [types.GET_USER]: state => state.user,

  [types.GET_STATS] (state) {
    const players = state.players.team;

    return {
      rating: getAverageRating(state),
      chemistry: Math.min(
        Math.max(
          0,
          state.players.team.reduce(
            (acc, player) => acc + player.chemistry.total,
            0
          )
        ),
        100
      ),

      attack: getAverageLine({ players, line: 'ATT' }),
      midfield: getAverageLine({ players, line: 'MID' }),
      defence: getAverageLine({ players, line: 'DEF' }),

      defensive: getAverageStat({ players, stat: 'rating_defensive' }),
      anchor: getAverageStat({ players, stat: 'rating_anchor' }),
      creative: getAverageStat({ players, stat: 'rating_creative' }),
      attacking: getAverageStat({ players, stat: 'rating_attacking' }),

      pace: getAverageStat({ players, stat: 'card_att_1' }),
      shooting: getAverageStat({ players, stat: 'card_att_2' }),
      passing: getAverageStat({ players, stat: 'card_att_3' }),
      dribbling: getAverageStat({ players, stat: 'card_att_4' }),
      defending: getAverageStat({ players, stat: 'card_att_5' }),
      physical: getAverageStat({ players, stat: 'card_att_6' }),
    };
  },
};

export const setupStore = ({
  awards,
  formation,
  initial,
  isEditable,
  isSbc,
  requirements,
  sbcId,
  share,
  title,
  user,
}) => {
  state.formation = formation;
  state.isEditable = isEditable;
  state.isSbc = isSbc;
  state.sbcAwards = awards;
  state.sbcId = sbcId;
  state.sbcRequirements = requirements;
  state.share = share;
  state.title = title;

  if (Object.keys(user).length > 0) {
    state.user = user;
  }

  if (initial.length > 0) {
    initial.forEach(([index, data]) => {
      const player = getPlayer(state, index);
      player.data = data;
      player.isFilled = true;
    });
  }

  updatePlayers({ formation, players: state.players.team });

  return new Vuex.Store({
    strict,
    state,
    mutations,
    actions,
    getters,
  });
};

function updatePlayers ({ formation, players }) {
  players.forEach(player => {
    player.isFilled = Object.keys(player.data).length > 0;
    player.positions.fromFormation =
      formationData[formation]['positions'][player.index];
    // prettier-ignore
    player.positions.inBuilder =
      allowedPositions[player.positions.fromFormation]
        .includes(player.data.position)
        ? player.positions.fromFormation
        : player.positions.inBuilder
          ? player.positions.inBuilder
          : player.data.position;
    player.positions.verbose =
      formationData[formation]['verbose'][player.index];

    player.formationLinks =
      formationData[formation].positionLinks[player.index];
    player.filledLinks = player.formationLinks.filter(
      link => state.players.team[link].isFilled
    );

    player.chemistry.links = calculateLinkChemistry(player, players);
    player.chemistry.positions = calculatePositionChemistry(player);
    player.chemistry.total = player.isFilled ? getTotalChem(player) || 0 : 0;
  });
}

function calculateLinkChemistry (player, team) {
  if (player.isFilled === false || player.filledLinks.length <= 0) {
    return 0.9;
  }

  let chemClub = 0;
  let chemLeague = 0;
  let chemNation = 0;

  for (const index of player.filledLinks) {
    const linkedPlayer = team[index];

    if (player.data.club.title === linkedPlayer.data.club.title) {
      chemClub++;
    }

    if (
      player.data.league.title === linkedPlayer.data.league.title ||
      [player.data.league.ea_id, linkedPlayer.data.league.ea_id].includes(2118)
    ) {
      chemLeague++;
    }

    if (player.data.nation.title === linkedPlayer.data.nation.title) {
      chemNation++;
    }
  }

  chemClub =
    player.filledLinks.length && chemClub / player.filledLinks.length * 3;
  chemLeague =
    player.filledLinks.length && chemLeague / player.filledLinks.length * 3;
  chemNation =
    player.filledLinks.length && chemNation / player.filledLinks.length * 3;

  const chemTotal = chemClub + chemLeague + chemNation;

  if (chemTotal >= 5) {
    return 3.5;
  } else if (chemTotal >= 3) {
    return 3;
  } else if (chemTotal >= 1) {
    return 2;
  } else {
    return 0.9;
  }
}

function calculatePositionChemistry (player) {
  const positionChemSchema = {
    strong: 3,
    good: 2.5,
    weak: 1.5,
    poor: 0.5,
  };
  const playerPosition = player.positions.inBuilder;

  if (playerPosition === player.positions.fromFormation) {
    return positionChemSchema.strong;
  } else if (
    goodChem.hasOwnProperty(player.positions.fromFormation) &&
    goodChem[player.positions.fromFormation].includes(playerPosition)
  ) {
    return positionChemSchema.good;
  } else if (
    weakChem.hasOwnProperty(player.positions.fromFormation) &&
    weakChem[player.positions.fromFormation].includes(playerPosition)
  ) {
    return positionChemSchema.weak;
  } else {
    return positionChemSchema.poor;
  }
}

const getGroup = index =>
  index <= 10 ? 'team' : index <= 17 ? 'bench' : 'reserves';
const getPlayer = (state, index) =>
  state.players[getGroup(index)].find(player => player.index === index);
const getTotalChem = player =>
  Math.min(
    10,
    Math.round(player.chemistry.links * player.chemistry.positions) +
      player.chemistry.boost
  );
const getAverageRating = state => {
  let players = state.isSbc
    ? state.players.team
    : Object.values(state.players).reduce((acc, arr) => acc.concat(arr));
  players = players.filter(player => player.isFilled && player.index < 18);
  const playersLength = players.length;
  let rating = players.reduce((total, player) => total + player.data.rating, 0);
  const average = rating / playersLength;

  if (average > 0) {
    players.forEach(player => {
      if (player.data.rating <= average) return;

      if (player.index <= 10) {
        rating += player.data.rating - average;
      } else {
        rating += Math.floor(0.5 * (player.data.rating - average));
      }
    });

    return Math.floor(rating / playersLength);
  }

  return 0;
};
