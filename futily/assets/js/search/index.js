import axios from 'axios'
import { debounce, map } from 'lodash'

class PlayerSearch {
  constructor ({ className }) {
    this.className = className
    const template = document.getElementById('PlayerSearchResult')
    const el = document.querySelector(className)

    this.els = {
      el,
      input: el.querySelector(`${className}_Input`),
      results: el.querySelector(`${className}_Results`),
      template: {
        el: template,
        result: template.content.querySelector('.plyr-SearchResult'),
        nation: template.content.querySelector('.plyr-SearchResult_Nation'),
        club: template.content.querySelector('.plyr-SearchResult_Club'),
        name: template.content.querySelector('.plyr-SearchResult_Name'),
        player: template.content.querySelector('.plyr-SearchResult_Player'),
        position: template.content.querySelector('.plyr-SearchResult_Position'),
        rating: template.content.querySelector('.plyr-SearchResult_Rating'),
        ratingIcon: template.content.querySelector(
          '.plyr-SearchResult_RatingIcon'
        )
      }
    }
    this._results = []

    this.handleInput = this.handleInput.bind(this)
    this.handleBodyPointerDown = this.handleBodyPointerDown.bind(this)

    this.setupListeners()
  }

  setupListeners () {
    const body = document.body || document.documentElement

    this.els.input.addEventListener('input', debounce(this.handleInput, 300))
    body.addEventListener('pointerdown', this.handleBodyPointerDown)
  }

  async handleInput (e) {
    /*
    We don't want to hit the API until the user has entered 3 characters.
    We also want to take in to account the times they delete their current
    search
    */
    if (e.target.value.length <= 2 && this.results.length) this.results = []
    if (e.target.value.length <= 2) return

    const { target } = e
    const { data } = await axios.get(this.getApiUrl(target.value))

    this.handleApiResults(data)
  }

  handleBodyPointerDown (e) {
    /* If the user has clicked anywhere but the search results, clear it */
    const { target } = e
    const isASearchResult = target.closest(this.className)

    if (!isASearchResult) {
      this.els.input.value = ''
      this.results = []
    }
  }

  handleApiResults ({ results }) {
    this.results = results
  }

  getApiUrl (query) {
    return `/api/players/?is_search=true&query=${query}`
  }

  createResult (data) {
    const className = `plyr-SearchResult plyr-SearchResult-${data.color}`

    this.els.template.nation.src = `/static/ea-images/nations/${data.nation
      .ea_id}.png`
    this.els.template.club.src = `/static/ea-images/clubs/${data.club
      .ea_id}.png`
    this.els.template.player.src = `/static/ea-images/players/${data.ea_id}.png`

    this.els.template.result.href = data.absolute_url
    this.els.template.result.className = className
    this.els.template.name.textContent = data.name
    this.els.template.position.textContent = `(${data.position})`
    this.els.template.rating.textContent = data.rating
    const clone = document.importNode(this.els.template.el.content, true)

    return clone
  }

  createResults (results) {
    const resultsFragment = document.createDocumentFragment()

    map(results, result =>
      resultsFragment.appendChild(this.createResult(result))
    )

    this.els.results.appendChild(resultsFragment)
  }

  destroyResults () {
    /*
    Cheap and easy way to delete all children nodes, we replace the
     existing results node we reference so we have to rebind this
     */
    const cNode = this.els.results.cloneNode(false)
    this.els.results.parentNode.replaceChild(cNode, this.els.results)
    this.els.results = cNode
  }

  get results () {
    return this._results
  }

  set results (val) {
    this._results = val

    this.destroyResults()

    const hasResult = val.length > 0
    this.els.results.setAttribute('aria-hidden', String(!hasResult))

    if (hasResult) {
      this.createResults(val)
    }
  }
}

export class HeaderPlayerSearch extends PlayerSearch {}

export class SectionPlayerSearch extends PlayerSearch {}

export class ComparePlayerSearch extends PlayerSearch {
  constructor ({ className }) {
    super({ className })

    this.baseUrl = this.els.el.dataset.baseUrl
  }

  createResult (data) {
    const className = `plyr-SearchResult plyr-SearchResult-${data.color}`

    this.els.template.nation.src = `/static/ea-images/nations/${data.nation
      .ea_id}.png`
    this.els.template.club.src = `/static/ea-images/clubs/${data.club
      .ea_id}.png`
    this.els.template.player.src = `/static/ea-images/players/${data.ea_id}.png`

    this.els.template.result.href = `${this.baseUrl}${data.id}/`
    this.els.template.result.className = className
    this.els.template.name.textContent = data.name
    this.els.template.position.textContent = `(${data.position})`
    this.els.template.rating.textContent = data.rating
    const clone = document.importNode(this.els.template.el.content, true)

    return clone
  }
}
