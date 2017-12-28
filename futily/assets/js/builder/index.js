import Vue from '../vue';
import { ApolloClient } from 'apollo-client';
import { HttpLink } from 'apollo-link-http';
import { InMemoryCache } from 'apollo-cache-inmemory';
import VueApollo from 'vue-apollo';

import Builder from './components/Builder.vue';
import { setupStore } from './store';

Vue.use(VueApollo);

const httpLink = new HttpLink({
  uri: '/api/graphql',
});

const apolloClient = new ApolloClient({
  link: httpLink,
  cache: new InMemoryCache(),
  connectToDevTools: true,
});

const apolloProvider = new VueApollo({
  defaultClient: apolloClient,
});

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
    apolloProvider,
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
