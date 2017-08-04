import { createFromAlgoliaCredentials } from 'vue-instantsearch'

import components from './components'

const searchStore = createFromAlgoliaCredentials(
  'Z68B2CP55T',
  'bd1f7df608bda1d496d1159dc0bb9605'
)
searchStore.indexName = 'player_index'

export default {
  components,

  data () {
    return {
      searchStore,
      searchEl: undefined,
      shouldSearchShow: false
    }
  },

  mounted () {
    this.searchEl = document.querySelector('.ais-input')

    document.addEventListener('pointerdown', e => {
      const { target } = e

      if (
        this.searchStore.results.length > 0 &&
        !target.closest('.sch-Players')
      ) {
        this.shouldSearchShow = false
      } else if (!this.shouldSearchShow && target === this.searchEl) {
        this.shouldSearchShow = true
      }
    })
  }
}
