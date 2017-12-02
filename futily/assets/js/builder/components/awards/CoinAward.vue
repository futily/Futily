<template>
  <div class="sbc-Award sbc-Award-coins">
    <img class="sbc-Award_Image" src="/static/ea-images/coins.png">
    <p class="sbc-Award_Text">
      {{ award.value }} coins
    </p>
  </div>
</template>

<script>
  export default {
    props: {
      award: Object,
    },
  };
</script>
