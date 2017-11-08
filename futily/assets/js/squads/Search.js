import axios from 'axios';
import { debounce } from '../utils';

export default class {
  constructor ({ el }) {
    const template = document.getElementById('PlayerCardResult');
    const _this = this;

    this.els = {
      el: el.querySelector('.bld-Search'),
      body: el.querySelector('.bld-Search_Body'),
      input: el.querySelector('.bld-Search_Input'),
      results: el.querySelector('.bld-Search_Results'),
      items: el.querySelector('.plyr-CardList_Items'),
      loading: el.querySelector('.bld-Search_Loading'),
      controls: {
        prev: el.querySelector('.bld-Search_Prev'),
        next: el.querySelector('.bld-Search_Next'),
      },
      template: {
        el: template,
        card: template.content.querySelector('.plyr-Card'),
        rating: template.content.querySelector('.plyr-Card_Rating'),
        position: template.content.querySelector('.plyr-Card_Position'),
        club: template.content.querySelector('.plyr-Card_Club'),
        nation: template.content.querySelector('.plyr-Card_Nation'),
        image: template.content.querySelector('.plyr-Card_Image'),
        name: template.content.querySelector('.plyr-Card_Name'),
        workrates: template.content.querySelector('.plyr-Card_Workrates'),
        skillMoves: template.content.querySelector(
          '.plyr-Card_Stars-skillMoves'
        ),
        weakFoot: template.content.querySelector('.plyr-Card_Stars-weakFoot'),
        stat1: {
          value: template.content.querySelector(
            '.plyr-Card_Stat-1 .plyr-Card_StatValue'
          ),
          key: template.content.querySelector(
            '.plyr-Card_Stat-1 .plyr-Card_StatKey'
          ),
        },
        stat2: {
          value: template.content.querySelector(
            '.plyr-Card_Stat-2 .plyr-Card_StatValue'
          ),
          key: template.content.querySelector(
            '.plyr-Card_Stat-2 .plyr-Card_StatKey'
          ),
        },
        stat3: {
          value: template.content.querySelector(
            '.plyr-Card_Stat-3 .plyr-Card_StatValue'
          ),
          key: template.content.querySelector(
            '.plyr-Card_Stat-3 .plyr-Card_StatKey'
          ),
        },
        stat4: {
          value: template.content.querySelector(
            '.plyr-Card_Stat-4 .plyr-Card_StatValue'
          ),
          key: template.content.querySelector(
            '.plyr-Card_Stat-4 .plyr-Card_StatKey'
          ),
        },
        stat5: {
          value: template.content.querySelector(
            '.plyr-Card_Stat-5 .plyr-Card_StatValue'
          ),
          key: template.content.querySelector(
            '.plyr-Card_Stat-5 .plyr-Card_StatKey'
          ),
        },
        stat6: {
          value: template.content.querySelector(
            '.plyr-Card_Stat-6 .plyr-Card_StatValue'
          ),
          key: template.content.querySelector(
            '.plyr-Card_Stat-6 .plyr-Card_StatKey'
          ),
        },
        chemistry: template.content.querySelector('.plyr-Card_ChemValue'),
      },
    };

    this.open = false;
    this.term = '';
    this.loading = false;
    this.index = null;
    this.results = [];
    this.pages = {
      _next: 0,
      _prev: 0,
      current: 1,
      total: 1,

      get next () {
        return this._next;
      },

      set next (val) {
        this._next = val;

        _this.els.controls.next.disabled = !this._next;
        _this.els.controls.next.classList.toggle(
          'bld-Search_Next-hidden',
          !this._next
        );
      },

      get prev () {
        return this._prev;
      },

      set prev (val) {
        this._prev = val;

        _this.els.controls.prev.disabled = !this._prev;
        _this.els.controls.prev.classList.toggle(
          'bld-Search_Prev-hidden',
          !this._prev
        );
      },
    };

    this.setupListeners();
  }

  setupListeners () {
    this.els.el.addEventListener('pointerdown', e => this.closeSearch());
    this.els.body.addEventListener('pointerdown', e => e.stopPropagation());

    this.els.input.addEventListener('pointerdown', e => e.stopPropagation());
    const searchHandler = async e => {
      this.loading = true;
      const { value } = e.target;
      if (value.length <= 2) return;

      this.term = value;
      Object.assign(this.pages, {
        next: '',
        prev: '',
        current: 1,
        total: 1,
      });
      this.results = await this.getResults(
        `/api/players?query=${this.term}&page=${this.pages.current}`
      );
    };
    this.els.input.addEventListener('input', debounce(searchHandler, 300));

    this.nextResults = this.nextResults.bind(this);
    this.prevResults = this.prevResults.bind(this);
    this.els.controls.next.addEventListener('click', this.nextResults);
    this.els.controls.prev.addEventListener('click', this.prevResults);

    this.els.results.addEventListener('click', e => {
      if (e.target.closest('.plyr-CardList_Item') === false) return;

      const target = e.target.closest('.plyr-CardList_Item');
      const index = this.els.resultEls.indexOf(target);

      const event = new CustomEvent('player:selected', {
        detail: {
          data: this.results[index],
          index: this.index,
          element: this.els.resultEls[index]
            .querySelector('.plyr-Card')
            .cloneNode(true),
        },
        bubbles: true,
      });
      this.els.el.dispatchEvent(event);
      this.closeSearch();
    });
  }

  startSearch (index) {
    this.open = true;
    this.index = index;
  }

  closeSearch () {
    this.open = false;
    this.term = '';
    this.results = [];
    Object.assign(this.pages, {
      next: '',
      prev: '',
      current: 1,
      total: 1,
    });
  }

  async getResults (url) {
    const res = await axios.get(url);
    const { data } = res;
    Object.assign(this.pages, {
      next: data.links.next ? data.pages.current + 1 : null,
      prev: data.links.previous ? data.pages.current - 1 : null,
      current: data.pages.current,
      total: data.pages.total,
    });

    this.loading = false;

    return data.results;
  }

  async nextResults (e) {
    e.stopPropagation();

    this.loading = true;

    this.results = await this.getResults(
      `/api/players?query=${this.term}&page=${this.pages.next}`
    );

    return this;
  }

  async prevResults (e) {
    e.stopPropagation();

    this.loading = true;

    this.results = await this.getResults(
      `/api/players?query=${this.term}&page=${this.pages.prev}`
    );

    return this;
  }

  createResult (data) {
    const className = `plyr-Card plyr-Card-medium plyr-Card-${data.color}`;

    this.els.template.nation.src = `/static/ea-images/nations/${data.nation
      .ea_id}.png`;
    this.els.template.club.src = `/static/ea-images/clubs/${data.club
      .ea_id}.png`;
    this.els.template.image.src = `/static/ea-images/players/${data.ea_id}.png`;

    this.els.template.el.setAttribute('tabindex', '0');
    this.els.template.card.className = className;
    this.els.template.rating.textContent = data.rating;
    this.els.template.position.textContent = data.position;
    this.els.template.name.textContent = data.name;
    this.els.template.workrates.textContent = `${data.work_rate_att[0]} / ${data
      .work_rate_def[0]}`;
    this.els.template.skillMoves.textContent = `${data.skill_moves}* SM`;
    this.els.template.weakFoot.textContent = `${data.weak_foot}* WF`;

    data.stats.map((stat, index) => {
      this.els.template[`stat${index + 1}`].key.textContent = stat[0];
      this.els.template[`stat${index + 1}`].value.textContent = stat[1];
    });

    this.els.template.chemistry.textContent = 0;

    return document.importNode(this.els.template.el.content, true);
  }

  createResults (results) {
    const resultsFragment = document.createDocumentFragment();

    results.map(result =>
      resultsFragment.appendChild(this.createResult(result))
    );

    this.els.items.appendChild(resultsFragment);
    this.els.resultEls = Array.from(
      this.els.items.querySelectorAll('.plyr-CardList_Item')
    );
  }

  destroyResults () {
    /*
    Cheap and easy way to delete all children nodes, we replace the
     existing results node we reference so we have to rebind this
     */
    const cNode = this.els.items.cloneNode(false);
    this.els.items.parentNode.replaceChild(cNode, this.els.items);
    this.els.items = cNode;
    this.els.resultEls = [];
  }

  get loading () {
    return this._loading;
  }

  set loading (val) {
    this._loading = val;

    this.els.loading.classList.toggle(
      'bld-Search_Loading-visible',
      this._loading
    );
    this.els.results.classList.toggle(
      'bld-Search_Results-loading',
      this._loading
    );
  }

  get open () {
    return this._open;
  }

  set open (val) {
    this._open = val;

    if (!this._open) this.index = null;
    this.els.el.setAttribute('aria-current', String(this._open));

    const listenerFnc = e => {
      const { target } = e;

      if (
        target.classList.contains('bld-Search') &&
        e.propertyName === 'visibility'
      ) {
        this.els.input.focus();

        target.removeEventListener('transitionend', listenerFnc);
      }
    };

    this.els.el.addEventListener('transitionend', listenerFnc);
  }

  get results () {
    return this._results;
  }

  set results (val) {
    this._results = val;

    this.destroyResults();

    if (this._results.length > 0) {
      this.createResults(this._results);
    }
  }

  get term () {
    return this._term;
  }

  set term (val) {
    this._term = val;

    this.els.input.value = this._term;
  }
}
