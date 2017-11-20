<template>
  <input type="hidden" name="csrftoken" :value="csrftoken">
</template>

<script>
  export default {
    data () {
      return {
        csrftoken: '',
      };
    },

    created () {
      const value = `; ${document.cookie}`;
      const parts = value.split(` csrftoken=`);
      if (parts.length === 2) this.csrftoken = parts.pop().split(';').shift();
    },
  };
</script>
