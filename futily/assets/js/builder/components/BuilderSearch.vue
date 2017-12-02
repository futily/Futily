<template>
  <div class="bld-Search" :aria-hidden="String(!search.open)" @click="closeSearch">
    <div class="bld-Search_Inner">
      <header class="bld-Search_Header">
        <span class="bld-Search_Icon">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52.966 52.966">
            <path d="M51.704 51.273L36.844 35.82c3.79-3.8 6.14-9.04 6.14-14.82 0-11.58-9.42-21-21-21s-21 9.42-21 21 9.42 21 21 21c5.082 0 9.747-1.817 13.383-4.832l14.895 15.49c.196.206.458.308.72.308.25 0 .5-.093.694-.28.398-.382.41-1.015.028-1.413zM21.984 40c-10.478 0-19-8.523-19-19s8.522-19 19-19 19 8.523 19 19-8.525 19-19 19z" />
          </svg>
        </span>

        <input class="bld-Search_Input"
               type="search"
               placeholder="Search for player"
               ref="input"
               :value="search.term"
               @click.stop
               @input="handleSearchInput" />
      </header>

      <div class="bld-Search_Body">
        <div :class="['bld-Search_Results', {'bld-Search_Results-loading': this.loading}]">
          <button rel="prev"
                  type="button"
                  :class="['bld-Search_Prev', {'bld-Search_Prev-hidden': hasPrev === false}]"
                  @click.stop="handlePrev"
                  :disabled="hasPrev === false">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 129 129">
              <path d="M88.6 121.3c.8.8 1.8 1.2 2.9 1.2s2.1-.4 2.9-1.2c1.6-1.6 1.6-4.2 0-5.8l-51-51 51-51c1.6-1.6 1.6-4.2 0-5.8s-4.2-1.6-5.8 0l-54 53.9c-1.6 1.6-1.6 4.2 0 5.8l54 53.9z" />
            </svg>
          </button>

          <div class="bld-Search_Items">
            <ul class="plyr-CardList_Items">
              <li class="plyr-CardList_Item"
                  v-for="result in search.results"
                  @click="handleResultsClick(result)">
                <PlayerCard :data="result" :position="result.position" :key="result.ea_id" />
              </li>
            </ul>
          </div>

          <button rel="next"
                  type="button"
                  :class="['bld-Search_Next', {'bld-Search_Next-hidden': hasNext === false}]"
                  @click.stop="handleNext"
                  :disabled="hasNext === false">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 129 129">
              <path d="M40.4 121.3c-.8.8-1.8 1.2-2.9 1.2s-2.1-.4-2.9-1.2c-1.6-1.6-1.6-4.2 0-5.8l51-51-51-51c-1.6-1.6-1.6-4.2 0-5.8 1.6-1.6 4.2-1.6 5.8 0l53.9 53.9c1.6 1.6 1.6 4.2 0 5.8l-53.9 53.9z" />
            </svg>
          </button>
        </div>
      </div>

      <div :class="['bld-Search_Loading', {'bld-Search_Loading-visible': this.loading}]">
        <span class="bld-Search_LoadingIcon">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
            <path d="M2.136 10c0-.568-.454-1.023-1.022-1.023C.544 8.977.09 9.432.09 10c0 .568.455 1.023 1.024 1.023.568 0 1.022-.455 1.022-1.023zm-.363 3.545c-.478.273-.66.91-.364 1.387.18.318.545.523.885.523.182 0 .34-.046.523-.137.5-.295.66-.91.387-1.386-.296-.5-.932-.66-1.432-.387zm4.272 3.273c-.477-.273-1.113-.113-1.386.364-.296.477-.115 1.113.363 1.386.16.09.34.137.522.137.364 0 .705-.182.887-.5.273-.478.113-1.114-.387-1.387zm12.16-3.25c-.478-.295-1.114-.113-1.387.364-.273.477-.113 1.113.364 1.386.16.09.34.137.523.137.363 0 .704-.182.886-.5.274-.455.092-1.09-.385-1.387zm-8.228 4.296c-.568 0-1.022.454-1.022 1.022 0 .57.454 1.023 1.022 1.023.568 0 1.023-.455 1.023-1.024 0-.568-.455-1.022-1.023-1.022zm3.932-1.046c-.478.273-.66.91-.365 1.387.182.318.546.522.887.522.182 0 .34-.045.523-.136.477-.272.66-.908.363-1.385-.295-.5-.91-.66-1.41-.387zM2.817 4.658c-.477-.294-1.113-.113-1.386.365-.273.5-.114 1.113.363 1.41.16.09.34.135.523.135.364 0 .705-.182.887-.5.272-.5.09-1.113-.387-1.41zm2.227-3.25c-.477.274-.66.91-.363 1.387.182.32.523.5.886.5.182 0 .34-.045.523-.136.478-.296.66-.91.365-1.387-.296-.478-.932-.637-1.41-.364zM10 .092c-.568 0-1.023.455-1.023 1.024 0 .568.455 1.022 1.023 1.022 4.34 0 7.864 3.523 7.864 7.864 0 .568.454 1.023 1.022 1.023.57 0 1.023-.455 1.023-1.023 0-5.455-4.455-9.91-9.91-9.91z" />
          </svg>
        </span>
      </div>
    </div>
  </div>
</template>

<script>
  import { mapActions, mapGetters, mapMutations } from 'vuex';

  import PlayerCard from './PlayerCard.vue';
  import * as types from '../types';
  import { debounce } from '../../utils';

  export default {
    components: {
      PlayerCard,
    },

    data () {
      return {
        loading: false,
      };
    },

    computed: {
      ...mapGetters({
        'search': types.GET_SEARCH,
      }),

      hasNext () {
        return this.search.pages.next !== null && this.search.pages.next > this.search.pages.current;
      },

      hasPrev () {
        return this.search.pages.prev !== null && this.search.pages.prev < this.search.pages.current;
      },
    },

    watch: {
      'search.open' (val) {
        if (val) {
          const listenerFnc = e => {
            const { target } = e;

            if (
              target.classList.contains('bld-Search') &&
              e.propertyName === 'visibility'
            ) {
              this.$refs.input.focus();

              target.removeEventListener('transitionend', listenerFnc);
            }
          };
          this.$el.addEventListener('transitionend', listenerFnc);
        }
      },
    },

    methods: {
      ...mapActions({
        'insertPlayer': types.INSERT_PLAYER,
      }),

      ...mapMutations({
        'closeSearch': types.CLOSE_SEARCH,
        'resetPages': types.RESET_SEARCH_PAGES,
        'setPages': types.SET_SEARCH_PAGES,
        'setResults': types.SET_SEARCH_RESULTS,
        'setTerm': types.SET_SEARCH_TERM,
      }),

      handleSearchInput: debounce(async function (evt) {
        const { value } = evt.target;
        if (value.length <= 2) return;

        this.loading = true;
        this.setTerm({ term: value });

        this.resetPages();
        this.setResults({
          results: await this.getResults(
            `/api/players?query=${this.search.term}&page=${this.search.pages.current}`,
          ),
        });
      }, 300),

      async getResults (url) {
        const res = await this.$http.get(url);
        const { data } = res;
        this.setPages({
          pages: {
            next: data.links.next ? data.pages.current + 1 : null,
            prev: data.links.previous ? data.pages.current - 1 : null,
            current: data.pages.current,
            total: data.pages.total,
          },
        });

        this.loading = false;

        return data.results;
      },

      handleResultsClick (data) {
        this.insertPlayer({ data });
      },

      async handleNext () {
        this.loading = true;

        this.setResults({
          results: await this.getResults(
            `/api/players?query=${this.search.term}&page=${this.search.pages.next}`,
          ),
        });
      },

      async handlePrev () {
        this.loading = true;

        this.setResults({
          results: await this.getResults(
            `/api/players?query=${this.search.term}&page=${this.search.pages.prev}`,
          ),
        });
      },
    },
  };
</script>
