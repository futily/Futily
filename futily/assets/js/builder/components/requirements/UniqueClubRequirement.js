import * as types from '../../types';
import { requirementMixin } from './mixin';

export default {
  name: 'UniqueClubRequirement',
  mixins: [requirementMixin],

  created () {
    this.$store.watch(() => {
      const players = this.$store.getters[types.GET_PLAYERS].team;
      this.currentValue = players
        .filter(player => player.isFilled)
        .reduce((acc, player) => {
          const id = player.data.club.ea_id;

          if (acc.includes(id) === false) {
            acc.push(id);
          }

          return acc;
        }, []).length;
    });
  },
};
