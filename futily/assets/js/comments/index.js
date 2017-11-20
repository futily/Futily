import Vue from 'vue';
import axios from 'axios';

import Comments from './components/Comments.vue';
import { setupStore } from './store';

Vue.prototype.$http = axios;

export default config => {
  new Vue({
    store: setupStore(config),
    render (h) {
      return h(Comments);
    },
  }).$mount('.js-Comments');
};
