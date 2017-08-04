import algoliasearch from 'algoliasearch'

export class PlayerSearch {
  constructor ({ el }) {
    this.els = {
      el: document,
      input: el.querySelector('.js-PlayerSearch_Input'),
      items: el.querySelector('.js-PlayerSearch_Items')
    }
    this.client = algoliasearch(
      'Z68B2CP55T',
      '65ca5b5d1fe117db0f3be17d3f1a9e25'
    )
    this.index = this.client.initIndex('player_index')

    this.els.input.addEventListener()
  }
}
