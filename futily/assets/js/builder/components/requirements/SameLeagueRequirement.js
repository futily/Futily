import * as types from '../../types';
import { requirementMixin } from './mixin';

export default {
  name: 'SameLeagueRequirement',
  mixins: [requirementMixin],

  created () {
    this.$store.watch(() => {
      const players = this.$store.getters[types.GET_PLAYERS].team;
      this.currentValue = Math.max(
        ...Object.values(
          players.filter(player => player.isFilled).reduce((acc, player) => {
            const id = player.data.league.ea_id;
            acc[id] = id in acc ? acc[id] + 1 : 1;

            return acc;
          }, {})
        )
      );
    });
  },
};
