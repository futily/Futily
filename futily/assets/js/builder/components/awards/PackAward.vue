<template>
  <div class="sbc-Award sbc-Award-pack">
    <div class="sbc-Award_Pack">
      <div :class="['pck-Pack_Pack', `pck-Pack_Pack-${award.pack.type}`]">
        <img class="pck-Pack_Player"
             :src="`/static/build/img/ea/packs/players/${availablePlayers}/${randomChoice}.png`"
             v-if="award.pack.type !== 'special'">
        <img class="pck-Pack_Player"
             src="/static/build/img/ea/packs/players/group/4.png"
             v-if="award.pack.type === 'special'">
      </div>
    </div>

    <p class="sbc-Award_Text">{{ award.pack.title }}</p>
  </div>
</template>

<script>
  export default {
    props: {
      award: Object,
    },

    computed: {
      availablePlayers () {
        return getRandomItem(['dele', 'griezemann', 'muller', 'ronaldo']);
      },

      randomChoice () {
        return getRandomItem([1, 2, 3]);
      },
    },
  };

  const getRandomItem = arr => arr[Math.floor(Math.random() * arr.length)];
</script>
