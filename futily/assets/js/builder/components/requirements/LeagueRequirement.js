import * as types from '../../types';
import { requirementMixin } from './mixin';

export default {
  name: 'LeagueRequirement',
  mixins: [requirementMixin],

  created () {
    this.$store.watch(() => {
      const players = this.$store.getters[types.GET_PLAYERS].team;
      this.currentValue = players
        .filter(player => player.isFilled)
        .filter(
          player => player.data.league.ea_id === this.requirement.leagueId
        ).length;
    });
  },
};
