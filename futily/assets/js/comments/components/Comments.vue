<template>
  <div class="cmm-Comments">
    <div class="cmm-Comments_Inner">
      <header class="cmm-Comments_Header">
        <h2 class="cmm-Comments_Title">Comments ({{ count }})</h2>

        <div class="cmm-Comments_Form" v-if="config.isAuthenticated">
          <CommentForm />
        </div>
      </header>

      <div class="cmm-Comments_Body">
        <ul class="cmm-Comments_Items">
          <li class="cmm-Comments_Item cmm-Comments_Item-odd" v-for="item in tree" :key="item.id">
            <CommentItem :data="item" />
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
  import { mapActions, mapGetters } from 'vuex';

  import CommentForm from './CommentForm.vue';
  import CommentItem from './CommentItem.vue';
  import * as types from '../types';

  export default {
    components: {
      CommentForm,
      CommentItem,
    },

    created () {
      this.loadComments();
    },

    computed: {
      ...mapGetters({
        'config': types.GET_CONFIG,
        'count': types.GET_COMMENT_COUNT,
        'tree': types.GET_TREE,
      }),
    },

    methods: {
      ...mapActions({
        'getCount': types.LOAD_COUNT,
        'loadComments': types.LOAD_COMMENTS,
      }),
    },
  };
</script>
