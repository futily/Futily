import * as types from '../../types';
import { requirementMixin } from './mixin';

export default {
  name: 'PlayerCountRequirement',
  mixins: [requirementMixin],

  created () {
    this.$store.watch(() => {
      const players = this.$store.getters[types.GET_PLAYERS].team;
      this.currentValue = players.filter(player => player.isFilled).length;
    });
  },
};
