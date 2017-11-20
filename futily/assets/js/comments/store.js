import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';

import * as types from './types';

Vue.use(Vuex);

const strict = process.env.NODE_ENV !== 'production';

const state = {
  config: {},
  tree: [],
  cids: [],
  newCids: [],
  count: 0,
};

const mutations = {
  [types.CREATE_TREE] (state, { data }) {
    const tree = [];
    const order = [];
    const comments = {};
    const children = {};
    const inCids = [];
    let curCids = [];
    let newCids = [];

    function getChildren (cid) {
      return children[cid].map(index => {
        if (comments[index].children === undefined) {
          comments[index].children = getChildren(index);
        }
        return comments[index];
      });
    }

    data.results.forEach(item => {
      inCids.push(item.id);
      comments[item.id] = item;

      if (item.level === 0) {
        order.push(item.id);
      }

      children[item.id] = [];

      if (item.parent_id !== item.id) {
        children[item.parent_id].push(item.id);
      }
    });

    order.forEach(id => {
      comments[id].children = getChildren(id);
      tree.push(comments[id]);
    });

    // Update attributes curcids and newcids.
    if (inCids.length) {
      if (state.cids.length) {
        inCids.forEach(id => {
          if (state.cids.includes(id)) {
            newCids.push(id);
          }

          curCids.push(id);
        });
      } else {
        curCids = inCids;
        newCids = [];
      }
    }

    state.tree = tree;
    state.cids = curCids;
    state.newCids = newCids;
    state.count = curCids.length;
  },

  [types.UPDATE_COUNT] (state, { count }) {
    state.count = count;
  },
};

const actions = {
  async [types.LOAD_COMMENTS] ({ commit, state }) {
    const res = await axios({
      url: state.config.listUrl,
      method: 'GET',
    });

    commit(types.CREATE_TREE, { data: res.data });
  },

  async [types.LOAD_COUNT] ({ commit, state }) {
    const res = await axios({
      url: state.config.countUrl,
      method: 'GET',
    });

    commit(types.UPDATE_COUNT, { count: res.data.count });
  },
};

const getters = {
  [types.GET_CONFIG]: state => state.config,
  [types.GET_COMMENT_COUNT]: state => state.count,
  [types.GET_TREE]: state => state.tree,
};

export const setupStore = config => {
  state.config = config;

  return new Vuex.Store({
    strict,
    state,
    mutations,
    actions,
    getters,
  });
};
