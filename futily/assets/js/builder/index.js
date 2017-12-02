import Vue from '../vue';
import Builder from './components/Builder.vue';
import { setupStore } from './store';

export default ({
  awards,
  formation,
  initial,
  isEditable,
  isSbc,
  page,
  requirements,
  saveUrl,
  sbcId,
  share,
  title,
  user,
}) => {
  return new Vue({
    store: setupStore({
      awards,
      formation,
      initial,
      isEditable,
      isSbc,
      requirements,
      share,
      sbcId,
      title,
      user,
    }),
    render (h) {
      return h(Builder, {
        props: {
          formation,
          page,
          saveUrl,
        },
      });
    },
  }).$mount('#js-Builder');
};
