import { Builder } from './Builder';
import {
  ChemistryRequirement,
  ClubRequirement,
  LeagueRequirement,
  NationRequirement,
  PlayerCountRequirement,
  RareCountRequirement,
  RatingRequirement,
  SameClubRequirement,
  SameLeagueRequirement,
  SameNationRequirement,
  UniqueClubRequirement,
  UniqueLeagueRequirement,
  UniqueNationRequirement
} from './requirements';

export class Challenge extends Builder {
  constructor ({ className, isEditable }) {
    super({ className, isEditable });

    const el = document.querySelector(`.${className}`);

    this.ajaxSave = !el.classList.contains('js-Builder-noAjax');
    this.className = className;

    this.els = Object.assign(this.els, {
      requirements: {
        el: el.querySelector('.js-Builder_Requirements'),
        items: el.querySelectorAll('.js-Builder_Requirement')
      },
      form: {
        chemistry: el.querySelector(`[name='chemistry']`),
        rating: el.querySelector(`[name='rating']`),
        loyalty: el.querySelector(`[name='loyalty']`),
        positionChanges: el.querySelector(`[name='position_changes']`)
      }
    });

    this.requirements = {
      // These will be looped over and called on player insertion, so we can keep the requirements
      // up to date
      fncs: [],
      // These will be the "values" of each requirement
      stats: {},
      get passed () {
        return (
          Object.keys(this.stats).length > 0 &&
          Object.values(this.stats).filter(stat => {
            return stat.passed;
          }).length === Object.keys(this.stats).length
        );
      }
    };

    this.setupRequirements();
  }

  setupRequirements () {
    const requirementSchema = Array.from(
      this.els.requirements.items
    ).map(item => ({
      el: item,
      data: JSON.parse(item.dataset.requirement)
    }));

    requirementSchema.forEach(requirement =>
      this.setupRequirement(requirement)
    );
  }

  setupRequirement (requirement) {
    const { el } = requirement;
    const { scope, type, value } = requirement.data;

    switch (type) {
      case 'chemistry':
        this.requirements.stats.chemistry = new ChemistryRequirement({
          el,
          scope,
          value
        });
        this.requirements.fncs.push(
          this.requirements.stats.chemistry.calculateValue.bind(
            null,
            this.players.team
          )
        );

        break;
      case 'rating':
        this.requirements.stats.rating = new RatingRequirement({
          el,
          scope,
          value
        });
        this.requirements.fncs.push(
          this.requirements.stats.rating.calculateValue.bind(
            null,
            this.players.team
          )
        );

        break;
      case 'club':
        this.requirements.stats.club = new ClubRequirement({
          el,
          scope,
          value,
          clubId: requirement.data.clubId
        });
        this.requirements.fncs.push(
          this.requirements.stats.club.calculateValue.bind(
            null,
            this.players.team
          )
        );

        break;
      case 'league':
        this.requirements.stats.league = new LeagueRequirement({
          el,
          scope,
          value,
          leagueId: requirement.data.leagueId
        });
        this.requirements.fncs.push(
          this.requirements.stats.league.calculateValue.bind(
            null,
            this.players.team
          )
        );

        break;
      case 'nation':
        this.requirements.stats.nation = new NationRequirement({
          el,
          scope,
          value,
          nationId: requirement.data.nationId
        });
        this.requirements.fncs.push(
          this.requirements.stats.nation.calculateValue.bind(
            null,
            this.players.team
          )
        );

        break;
      case 'rares':
        this.requirements.stats.rares = new RareCountRequirement({
          el,
          scope,
          value
        });
        this.requirements.fncs.push(
          this.requirements.stats.rares.calculateValue.bind(
            null,
            this.players.team
          )
        );

        break;
      case 'player_count':
        this.requirements.stats.playerCount = new PlayerCountRequirement({
          el,
          scope,
          value
        });
        this.requirements.fncs.push(
          this.requirements.stats.playerCount.calculateValue.bind(
            null,
            this.players.team
          )
        );

        break;
      case 'same_club':
        this.requirements.stats.sameClub = new SameClubRequirement({
          el,
          scope,
          value
        });
        this.requirements.fncs.push(
          this.requirements.stats.sameClub.calculateValue.bind(
            null,
            this.players.team
          )
        );

        break;
      case 'same_league':
        this.requirements.stats.sameLeague = new SameLeagueRequirement({
          el,
          scope,
          value
        });
        this.requirements.fncs.push(
          this.requirements.stats.sameLeague.calculateValue.bind(
            null,
            this.players.team
          )
        );

        break;
      case 'same_nation':
        this.requirements.stats.sameNation = new SameNationRequirement({
          el,
          scope,
          value
        });
        this.requirements.fncs.push(
          this.requirements.stats.sameNation.calculateValue.bind(
            null,
            this.players.team
          )
        );

        break;
      case 'unique_club':
        this.requirements.stats.sameClub = new UniqueClubRequirement({
          el,
          scope,
          value
        });
        this.requirements.fncs.push(
          this.requirements.stats.sameClub.calculateValue.bind(
            null,
            this.players.team
          )
        );

        break;
      case 'unique_league':
        this.requirements.stats.sameLeague = new UniqueLeagueRequirement({
          el,
          scope,
          value
        });
        this.requirements.fncs.push(
          this.requirements.stats.sameLeague.calculateValue.bind(
            null,
            this.players.team
          )
        );

        break;
      case 'unique_nation':
        this.requirements.stats.sameNation = new UniqueNationRequirement({
          el,
          scope,
          value
        });
        this.requirements.fncs.push(
          this.requirements.stats.sameNation.calculateValue.bind(
            null,
            this.players.team
          )
        );

        break;
    }
  }

  insertPlayer ({ data, element, index }) {
    super.insertPlayer({ data, element, index });

    this.requirements.fncs.forEach(fnc => fnc());

    this.els.form.chemistry.value = Math.min(
      Math.max(
        0,
        this.players.team.reduce((acc, player) => {
          acc += player.chemistry.total;

          return acc;
        }, 0)
      ),
      100
    );
    this.els.form.rating.value = this.getAverageStat({
      players: this.players.team,
      stat: 'rating',
      includeGk: true
    });
    this.els.form.loyalty.value = this.players.team.filter(
      player => player.isFilled && player.chemistry.boost === 1
    ).length;
    this.els.form.positionChanges.value = this.players.team.filter(
      player =>
        player.isFilled && player.data.position !== player.positions.inBuilder
    ).length;
  }

  async handleSubmit (e) {
    if (this.requirements.passed) {
      await super.handleSubmit(e);
    } else {
      e.preventDefault();

      alert(
        'All requirements need to be passing before the squad can be submitted.'
      );
    }
  }
}
