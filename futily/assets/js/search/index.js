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
    this._activeResult = -1
    this.currentEvent = null
    this.resultEls = []
    this.resultHeight = 0
    this.resultsHeight = this.els.results.offsetHeight

    this.handleInput = this.handleInput.bind(this)
    this.handleBodyPointerDown = this.handleBodyPointerDown.bind(this)
    this.handlePointerOver = this.handlePointerOver.bind(this)
    this.handlePointerLeave = this.handlePointerLeave.bind(this)
    this.handleKeyDown = this.handleKeyDown.bind(this)

    this.setupListeners()
  }

  setupListeners () {
    const body = document.body || document.documentElement

    this.els.input.addEventListener('input', debounce(this.handleInput, 300))
    body.addEventListener('pointerdown', this.handleBodyPointerDown)

    this.els.el.addEventListener('pointerover', this.handlePointerOver)
    this.els.el.addEventListener('pointerleave', this.handlePointerLeave)
    this.els.el.addEventListener('keydown', this.handleKeyDown)
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

  handlePointerOver (e) {
    const item = e.target.closest('.plyr-SearchResults_Result')
    const index = this.resultEls.indexOf(item)
    if (index === this.activeResult) return

    this.activeResult = index
    this.currentEvent = 'pointer'
  }

  handlePointerLeave (e) {
    if (e.target !== this.els.el) return

    this.activeResult = -1
  }

  handleKeyDown (e) {
    const { keyCode } = e
    const keyMap = {
      13: 'enter',
      38: 'up',
      40: 'down'
    }
    const handleEnterKey = () => {
      this.resultEls[this.activeResult]
        .querySelector('.plyr-SearchResult')
        .click()
    }
    const handleArrowKey = () => {
      this.activeResult =
        keyMap[keyCode] === 'up' ? this.activeResult - 1 : this.activeResult + 1
    }

    if (
      !this.results.length ||
      !Object.keys(keyMap).includes(String(keyCode))
    ) {
      return
    }

    this.currentEvent = 'keyboard'
    ;[38, 40].includes(keyCode) ? handleArrowKey() : handleEnterKey()
  }

  handleApiResults ({ results }) {
    this.results = results
  }

  handleResultOverflow () {
    this.els.results.scrollTop =
      this.resultPosition >= this.resultsHeight - this.els.results.scrollTop
        ? this.resultPosition - this.resultsHeight
        : 0
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

    this.els.template.el.setAttribute('tabindex', '0')
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
    this.resultEls = Array.from(
      this.els.results.querySelectorAll('.plyr-SearchResults_Result')
    )
    this.resultHeight = this.resultEls[0].offsetHeight
    this.resultsHeight = this.els.results.offsetHeight
  }

  destroyResults () {
    /*
    Cheap and easy way to delete all children nodes, we replace the
     existing results node we reference so we have to rebind this
     */
    const cNode = this.els.results.cloneNode(false)
    this.els.results.parentNode.replaceChild(cNode, this.els.results)
    this.els.results = cNode
    this.els.resultEls = []
    this.activeResult = -1
  }

  get resultPosition () {
    return (this.activeResult + 1) * this.resultHeight
  }

  get activeResult () {
    return this._activeResult
  }

  set activeResult (val) {
    if (this._activeResult != null && this._activeResult >= 0) {
      this.resultEls[this._activeResult].classList.remove(
        'plyr-SearchResults_Result-active'
      )
    }

    const wantsToGoBelowMinumum = val => val < -1
    const wantsToGoAboveMaximum = val => val > this.results.length - 1

    this._activeResult = wantsToGoBelowMinumum(val)
      ? -1
      : wantsToGoAboveMaximum(val) ? this.results.length - 1 : val

    if (this.activeResult >= 0) {
      this.resultEls[this.activeResult].classList.add(
        'plyr-SearchResults_Result-active'
      )

      if (this.currentEvent === 'keyboard') {
        this.handleResultOverflow()
      }
    }
  }

  get results () {
    return this._results
  }

  set results (val) {
    this._results = val

    this.destroyResults()

    const hasResult = this._results.length > 0
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

export class SettingsPlayerSearch extends PlayerSearch {
  constructor ({ className }) {
    super({ className })

    this.input = document.querySelector(
      `[name=${this.els.el.dataset.inputField}]`
    )
    this.playerEl = document.querySelector('.frm-Form_Extra-player')
  }

  createResult (data) {
    const className = `plyr-SearchResult plyr-SearchResult-${data.color}`

    this.els.template.nation.src = `/static/ea-images/nations/${data.nation
      .ea_id}.png`
    this.els.template.club.src = `/static/ea-images/clubs/${data.club
      .ea_id}.png`
    this.els.template.player.src = `/static/ea-images/players/${data.ea_id}.png`

    this.els.template.result.dataset.playerId = data.id
    this.els.template.result.className = className
    this.els.template.name.textContent = data.name
    this.els.template.position.textContent = `(${data.position})`
    this.els.template.rating.textContent = data.rating
    const clone = document.importNode(this.els.template.el.content, true)

    return clone
  }

  get resultEls () {
    return this._resultEls
  }

  set resultEls (val) {
    this._resultEls = val

    if (this._resultEls.length > 0) {
      Array.from(this._resultEls).map(el => {
        el.addEventListener('click', e => {
          e.preventDefault()

          const wantedTarget = e.target.closest('.plyr-SearchResult')
          const wantedClone = wantedTarget.cloneNode(true)
          this.input.value = wantedTarget.dataset.playerId
          this.playerEl.innerHTML = ''
          this.playerEl.appendChild(wantedClone)

          this.els.input.value = ''
          this.results = []
        })
      })
    }
  }
}

export class SettingsObjectSearch extends PlayerSearch {
  constructor ({ className, object = '' }) {
    super({ className })

    this.getTemplate()

    this.input = document.querySelector(
      `[name=${this.els.el.dataset.inputField}]`
    )
    this.objectEl = document.querySelector(`.frm-Form_Extra-${object}`)
  }

  get resultEls () {
    return this._resultEls
  }

  set resultEls (val) {
    this._resultEls = val

    if (this._resultEls.length > 0) {
      Array.from(this._resultEls).map(el => {
        el.addEventListener('click', e => {
          e.preventDefault()

          const wantedTarget = e.target.closest('.plyr-SearchResult')
          const wantedClone = wantedTarget.cloneNode(true)
          this.input.value = wantedTarget.dataset.objectId
          this.objectEl.innerHTML = ''
          this.objectEl.appendChild(wantedClone)

          this.els.input.value = ''
          this.results = []
        })
      })
    }
  }
}

export class SettingsClubSearch extends SettingsObjectSearch {
  constructor ({ className }) {
    super({ className, object: 'club' })
  }

  getApiUrl (query) {
    return `/api/clubs/?query=${query}`
  }

  getTemplate () {
    const template = document.getElementById('ClubSearchResult')

    this.els.template = {
      el: template,
      result: template.content.querySelector('.plyr-SearchResult'),
      club: template.content.querySelector('.plyr-SearchResult_Club'),
      name: template.content.querySelector('.plyr-SearchResult_Name')
    }

    return template
  }

  createResult (data) {
    const className = `plyr-SearchResult plyr-SearchResult-object`

    this.els.template.club.src = `/static/ea-images/clubs/${data.ea_id}.png`

    this.els.template.result.dataset.objectId = data.id
    this.els.template.result.className = className
    this.els.template.name.textContent = data.name
    const clone = document.importNode(this.els.template.el.content, true)

    return clone
  }
}

export class SettingsNationSearch extends SettingsObjectSearch {
  constructor ({ className }) {
    super({ className, object: 'nation' })
  }

  getApiUrl (query) {
    return `/api/nations/?query=${query}`
  }

  getTemplate () {
    const template = document.getElementById('NationSearchResult')

    this.els.template = {
      el: template,
      result: template.content.querySelector('.plyr-SearchResult'),
      nation: template.content.querySelector('.plyr-SearchResult_Nation'),
      name: template.content.querySelector('.plyr-SearchResult_Name')
    }

    return template
  }

  createResult (data) {
    const className = `plyr-SearchResult plyr-SearchResult-object`

    this.els.template.nation.src = `/static/ea-images/nations/${data.ea_id}.png`

    this.els.template.result.dataset.objectId = data.id
    this.els.template.result.className = className
    this.els.template.name.textContent = data.name
    const clone = document.importNode(this.els.template.el.content, true)

    return clone
  }
}
