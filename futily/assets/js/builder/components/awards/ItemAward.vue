<template>
  <PlayerCard :data="player" :isLinked="true" :position="player.position" v-if="award.isPlayer" />
  <div v-else>
    Item {{ award.value }}
  </div>
</template>

<script>
  import PlayerCard from '../PlayerCard';

  export default {
    components: {
      PlayerCard,
    },

    props: {
      award: Object,
    },

    data () {
      return {
        player: {},
      };
    },

    created () {
      if (this.award.isPlayer) {
        this.$http.get(`/api/players/${this.award.value}/`)
          .then(res => {
            this.player = res.data;
          });
      }
    },
  };
</script>
