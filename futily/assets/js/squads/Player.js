import allowedPositions from './allowedPositions';
import formationData from './formationData';
import { Cycler } from '../utils';
import { goodChem, weakChem } from './chemPosition';

export class Player {
  constructor ({ index, el, isEditable, initialData = {} }) {
    this.isEditable = isEditable;

    this.els = {
      el,
      player: el.querySelector('.bld-Slot'),
      pedestal: el.querySelector('.bld-Slot_Pedestal'),
    };

    this.index = index;

    this.links = [];
    this.filledLinks = [];

    this._card = null;
    this.data = initialData;
    this.chemistry = this.constructChemistry();
    this.positions = this.constructPositions();

    this.coords = this.getCoordinates();
  }

  getCoordinates () {
    const style = window.getComputedStyle(this.els.el).transform;
    const match = style.match(/^matrix\((.+)\)$/)[1].split(',');
    const x =
      this.els.el.offsetLeft +
      parseFloat(match[4]) +
      this.els.el.offsetWidth / 2;
    const y =
      this.els.el.offsetTop +
      parseFloat(match[5]) +
      (this.els.el.offsetHeight / 2 + 100);

    return {
      x,
      y,
    };
  }

  calculateLinkChemistry (team) {
    if (this.filledLinks.length <= 0) {
      this.chemistry.links = 0.9;

      return;
    }

    let chemClub = 0;
    let chemLeague = 0;
    let chemNation = 0;

    for (const index of this.filledLinks) {
      const linkedPlayer = team[index];

      if (this.data.club.title === linkedPlayer.data.club.title) {
        chemClub++;
      }

      if (
        this.data.league.title === linkedPlayer.data.league.title ||
        [this.data.league.ea_id, linkedPlayer.data.league.ea_id].includes(2118)
      ) {
        chemLeague++;
      }

      if (this.data.nation.title === linkedPlayer.data.nation.title) {
        chemNation++;
      }
    }

    chemClub =
      this.filledLinks.length && chemClub / this.filledLinks.length * 3;
    chemLeague =
      this.filledLinks.length && chemLeague / this.filledLinks.length * 3;
    chemNation =
      this.filledLinks.length && chemNation / this.filledLinks.length * 3;

    const chemTotal = chemClub + chemLeague + chemNation;

    if (chemTotal >= 5) {
      this.chemistry.links = 3.5;
    } else if (chemTotal >= 3) {
      this.chemistry.links = 3;
    } else if (chemTotal >= 1) {
      this.chemistry.links = 2;
    } else {
      this.chemistry.links = 0.9;
    }
  }

  calculateIndividualLinkChemistry (target) {
    if (
      Object.keys(target.data).length === 0 ||
      Object.keys(this.data).length === 0
    ) {
      return 0;
    }

    let chemClub = 0;
    let chemLeague = 0;
    let chemNation = 0;

    if (this.data.club.title === target.data.club.title) {
      chemClub++;
    }

    if (
      this.data.league.title === target.data.league.title ||
      [this.data.league.ea_id, target.data.league.ea_id].includes(2118)
    ) {
      chemLeague++;
    }

    if (this.data.nation.title === target.data.nation.title) {
      chemNation++;
    }

    return chemClub + chemLeague + chemNation;
  }

  calculatePositionChemistry () {
    const positionChemSchema = {
      strong: 3,
      good: 2.5,
      weak: 1.5,
      poor: 0.5,
    };
    const playerPosition = this.positions.inBuilder;

    if (playerPosition === this.positions.fromFormation) {
      this.chemistry.position = positionChemSchema.strong;
    } else if (
      goodChem.hasOwnProperty(this.positions.fromFormation) &&
      goodChem[this.positions.fromFormation].includes(playerPosition)
    ) {
      this.chemistry.position = positionChemSchema.good;
    } else if (
      weakChem.hasOwnProperty(this.positions.fromFormation) &&
      weakChem[this.positions.fromFormation].includes(playerPosition)
    ) {
      this.chemistry.position = positionChemSchema.weak;
    } else {
      this.chemistry.position = positionChemSchema.poor;
    }
  }

  constructChemistry () {
    const _this = this;

    return {
      _links: 0,
      get links () {
        return this._links;
      },

      set links (val) {
        this._links = val;

        if (_this.isEditable) {
          _this.card.querySelector(
            '.plyr-Card_ChemValue'
          ).innerText = this.total;
          _this.setFormData();
        }
      },
      _position: 0,
      get position () {
        return this._position;
      },

      set position (val) {
        this._position = val;

        if (_this.isEditable) {
          _this.card.querySelector(
            '.plyr-Card_ChemValue'
          ).innerText = this.total;
          _this.setFormData();
        }
      },
      _boost: 0,
      get boost () {
        return this._boost;
      },

      set boost (val) {
        this._boost = val;

        if (_this.isEditable) {
          _this.card.querySelector(
            '.plyr-Card_ChemValue'
          ).innerText = this.total;
          _this.setFormData();
        }
      },

      get total () {
        const roundedChem = Math.round(this.links * this.position);

        return Math.min(10, roundedChem + this.boost);
      },
    };
  }

  constructPositions () {
    const _this = this;

    return {
      _fromFormation: '',
      get fromFormation () {
        return this._fromFormation;
      },
      set fromFormation (val) {
        this._fromFormation = val;

        _this.els.pedestal.innerText = this._fromFormation;
      },

      _inBuilder: '',
      get inBuilder () {
        return this._inBuilder;
      },
      set inBuilder (val) {
        this._inBuilder = val;

        if (this._inBuilder) {
          _this.card.querySelector(
            '.plyr-Card_Position'
          ).innerText = this._inBuilder;
          _this.calculatePositionChemistry();
        }
      },

      _verbose: '',
      get verbose () {
        return this._verbose;
      },
      set verbose (val) {
        this._verbose = val;

        _this.els.el.className = `js-Builder_PlayersItem bld-Builder_PlayersItem bld-Builder_PlayersItem-${this._verbose.toLowerCase()}`;
      },
    };
  }

  setLinks ({ formation, team }) {
    this.links = formationData[formation].positionLinks[this.index];
    this.filledLinks = this.links.filter(link => team[link].isFilled);
    this.coords = this.getCoordinates();
  }

  setPosition (key, position) {
    this.positions[key] = position;
  }

  get isFilled () {
    return Object.keys(this.data).length !== 0;
  }
}

export class EditablePlayer extends Player {
  constructor ({ index, el, isEditable, initialCard, initialData = {} }) {
    super({ index, el, isEditable, initialData });

    this.els = Object.assign(this.els, {
      input: el.querySelector('.bld-Builder_PlayerInput'),
      controls: {
        el: el.querySelector('.bld-Slot_Controls'),
        remove: el.querySelector('.bld-Slot_Control-remove'),
        changePosition: el.querySelector('.bld-Slot_Control-changePosition'),
        toggleLoyalty: el.querySelector('.bld-Slot_Control-toggleLoyalty'),
      },
    });
    this._card = initialCard;

    this.positionsCycle = null;

    this.setupListeners();
  }

  setupListeners () {
    this.els.controls.el.addEventListener('pointerdown', e =>
      e.stopPropagation()
    );

    this.els.controls.remove.addEventListener('pointerdown', () => {
      const event = new CustomEvent('player:removed', {
        detail: {
          index: this.index,
        },
        bubbles: true,
      });
      this.els.el.dispatchEvent(event);
    });

    this.els.controls.toggleLoyalty.addEventListener('pointerdown', () => {
      this.chemistry.boost = this.chemistry.boost === 1 ? 0 : 1;
    });

    this.els.controls.changePosition.addEventListener('pointerdown', () => {
      this.cyclePositions();
    });
  }

  cyclePositions () {
    this.positions.inBuilder = this.positionsCycle.next();
  }

  constructPlayer ({ data, element }) {
    this.card = element;
    this.data = data;
    this.setInBuilderPosition();
    this.els.el.dataset.builderFilled = 'true';
    this.positionsCycle = new Cycler({
      items: allowedPositions[this.positions.inBuilder],
      currentPosition: allowedPositions[this.positions.inBuilder].indexOf(
        this.positions.inBuilder
      ),
    });
    this.setFormData();
  }

  cloneCard () {
    return this.isFilled
      ? this.els.el.querySelector('.plyr-Card').cloneNode(true)
      : null;
  }

  removePlayer () {
    this.card = null;
    this.data = {};
    this.els.input.value = '';
    this.positions.inBuilder = '';
    this.chemistry = this.constructChemistry();
    this.els.el.dataset.builderFilled = 'false';
  }

  setFormData () {
    this.els.input.value = `${this.data.id},${this.index},${this.positions
      .inBuilder},${this.chemistry.total}`;
  }

  setInBuilderPosition () {
    this.setPosition(
      'inBuilder',
      allowedPositions[this.positions.fromFormation].includes(
        this.data.position
      )
        ? this.positions.fromFormation
        : this.data.position
    );
  }

  setPosition (key, position) {
    this.positions[key] = position;
  }

  get card () {
    return this._card;
  }

  set card (val) {
    this._card = val;

    this.els.player.innerHTML = '';

    if (this._card) {
      this.els.player.appendChild(this._card);
    }
  }
}
