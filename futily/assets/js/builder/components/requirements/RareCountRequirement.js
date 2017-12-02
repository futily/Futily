import * as types from '../../types';
import { RARE_COLOURS } from '../../utils/constants';
import { requirementMixin } from './mixin';

export default {
  name: 'RareCountRequirement',
  mixins: [requirementMixin],

  created () {
    this.$store.watch(() => {
      const players = this.$store.getters[types.GET_PLAYERS].team;
      this.currentValue = players.filter(
        player => player.isFilled && RARE_COLOURS.includes(player.data.color)
      ).length;
    });
  },
};
