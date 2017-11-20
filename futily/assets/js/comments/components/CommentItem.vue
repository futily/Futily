<template>
  <div class="cmm-Item">
    <header class="cmm-Item_Header">
      <Comment :data="data" />
    </header>

    <footer class="cmm-Item_Footer" v-if="false">
      <button class="cmm-Item_LoadMore">
        Load more

        <span class="cmm-Item_LoadMoreIcon">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 284.929 284.929">
            <path d="M282.082 76.51L267.808 62.24c-1.902-1.906-4.093-2.856-6.57-2.856-2.47 0-4.66.95-6.563 2.856L142.465 174.44 30.263 62.24c-1.903-1.905-4.093-2.855-6.567-2.855-2.475 0-4.665.95-6.567 2.856L2.856 76.516C.95 78.417 0 80.607 0 83.082c0 2.473.953 4.663 2.856 6.565L135.9 222.693c1.9 1.903 4.092 2.854 6.566 2.854s4.66-.95 6.562-2.854L282.082 89.647c1.902-1.903 2.847-4.093 2.847-6.565 0-2.475-.946-4.665-2.848-6.57z" />
          </svg>
        </span>
      </button>
    </footer>

    <div class="cmm-Item_Children" v-if="data.children.length > 0">
      <ul class="cmm-Comments_Items">
        <li :class="['cmm-Comments_Item', `cmm-Comments_Item-${item.level % 2 ? 'even' : 'odd'}`]"
            :key="item.id"
            v-for="item in data.children">
          <CommentItem :data="item" />
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
  import Comment from './Comment.vue';

  export default {
    name: 'CommentItem',

    components: {
      Comment,
    },

    props: {
      data: Object,
    },
  };
</script>
