<template>
  <a :href="`/players/${result.id}-${result.slug}`" class="ais-result">
    <ais-highlight :result="result" attribute-name="name"></ais-highlight> ({{ result.rating }})
  </a>
</template>

<script>
  export default {
    props: {
      result: {
        type: Object,
        required: true
      }
    }
  }
</script>
