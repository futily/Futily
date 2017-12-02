import * as types from '../../types';
import { requirementMixin } from './mixin';

export default {
  name: 'ClubRequirement',
  mixins: [requirementMixin],

  created () {
    this.$store.watch(() => {
      const players = this.$store.getters[types.GET_PLAYERS].team;
      this.currentValue = players
        .filter(player => player.isFilled)
        .filter(
          player => player.data.club.ea_id === this.requirement.clubId
        ).length;
    });
  },
};
