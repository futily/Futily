import * as types from '../../types';
import { requirementMixin } from './mixin';

export default {
  name: 'ChemistryRequirement',
  mixins: [requirementMixin],

  created () {
    this.$store.watch(() => {
      const stats = this.$store.getters[types.GET_STATS];
      this.currentValue = stats.chemistry;
    });
  },
};
