import * as types from '../../types';
import { requirementMixin } from './mixin';

export default {
  name: 'NationRequirement',
  mixins: [requirementMixin],

  created () {
    this.$store.watch(() => {
      const players = this.$store.getters[types.GET_PLAYERS].team;
      this.currentValue = players
        .filter(player => player.isFilled)
        .filter(
          player => player.data.nation.ea_id === this.requirement.nationId
        ).length;
    });
  },
};
