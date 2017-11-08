import { getAverageStat } from './utils';
import { RARE_COLOURS } from './constants';

class Requirement {
  constructor ({ el, scope, value }) {
    this.els = {
      el,
      data: el.querySelector('.js-Builder_RequirementData'),
      current: el.querySelector('.js-Builder_RequirementCurrent'),
      completed: el.querySelector('.js-Builder_RequirementCompleted')
    };

    this.required = value;
    this.scope = scope;

    this.calculateValue = this.calculateValue.bind(this);
  }

  calculateValue () {
    throw new Error('This method needs to be implemented');
  }

  setValue (val) {
    this.value = val;

    this.els.current.innerText = val;

    this.els.completed.innerHTML = this.passed
      ? `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 496.158 496.158">
    <path d="M496.2 248c0-137-111-248-248-248S0 111 0 248s111 248.2 248 248.2 248.2-111 248.2-248z" fill="#32BEA6"/>
    <path d="M384.7 165c-6-15-17.8-12.7-30.7-10.2-7.7 1.6-42 11.7-96 68.8-22.6 23.7-37.4 42.6-47.2 57-6-7.3-12.8-15-20-22.3-22-22-46.7-37.2-47.7-38-10-6.2-23-3-30 7.4-6 10.3-3 23.8 8 30.2 0 0 21.5 13 39.8 31 18.6 18 35.5 44 35.6 44 4 6 11 10 18.3 10 1.3 0 2.5 0 3.8-1 8.6-1.6 15.5-8 17.6-16.4 0-.3 9-24.3 55-72.8 37-39 61.7-51.5 70-55h.6l1-.4 2.3-.8h-.7l11.4-5c11-4.7 14.8-16.7 10.5-28z" fill="#FFF"/>
</svg>`
      : `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 496.158 496.158">
    <path d="M496.2 248c0-137-111-248-248-248S0 111 0 248s111 248.2 248 248.2 248.2-111 248.2-248z" fill="#E04F5F"/>
    <path d="M277 248l72.6-84c8-9.3 6.8-23.2-2.3-31-9.2-8-23-7-31 2.2L248 214.5l-68-79.3c-8-9-21.7-10.2-31-2.3-9 7.6-10 21.5-2.2 31l72.5 84-72.3 84c-8 9.2-7 23 2.2 31 4 3.5 9 5.2 14.2 5.2 6.2 0 12.3-2.5 16.6-7.6l68.3-79.3 68.3 79.2c4.4 5 10.5 7.5 16.7 7.5 5 0 10-1.7 14.3-5.3 9-8 10.2-21.8 2.3-31l-72.8-84z" fill="#FFF"/>
</svg>`;
  }

  get passed () {
    return this.scope === 'gte'
      ? this.value >= this.required
      : this.scope === 'lte'
        ? this.value <= this.required
        : this.value === this.required;
  }
}

export class ChemistryRequirement extends Requirement {
  calculateValue (players) {
    this.setValue(
      Math.min(
        Math.max(
          0,
          players.reduce((acc, player) => {
            acc += player.chemistry.total;

            return acc;
          }, 0)
        ),
        100
      )
    );
  }
}

export class RatingRequirement extends Requirement {
  calculateValue (players) {
    this.setValue(
      getAverageStat({
        players,
        stat: 'rating',
        includeGk: true
      })
    );
  }
}

export class ClubRequirement extends Requirement {
  constructor ({ el, scope, value, clubId }) {
    super({ el, scope, value });

    this.clubId = clubId;
  }

  calculateValue (players) {
    this.setValue(
      players.filter(
        player => player.isFilled && player.data.club.ea_id === this.clubId
      ).length
    );
  }
}

export class LeagueRequirement extends Requirement {
  constructor ({ el, scope, value, leagueId }) {
    super({ el, scope, value });

    this.leagueId = leagueId;
  }

  calculateValue (players) {
    this.setValue(
      players.filter(
        player => player.isFilled && player.data.league.ea_id === this.leagueId
      ).length
    );
  }
}

export class NationRequirement extends Requirement {
  constructor ({ el, scope, value, nationId }) {
    super({ el, scope, value });

    this.nationId = nationId;
  }

  calculateValue (players) {
    this.setValue(
      players.filter(
        player => player.isFilled && player.data.nation.ea_id === this.nationId
      ).length
    );
  }
}

export class RareCountRequirement extends Requirement {
  calculateValue (players) {
    this.setValue(
      players.filter(
        player => player.isFilled && RARE_COLOURS.includes(player.data.color)
      ).length
    );
  }
}

export class PlayerCountRequirement extends Requirement {
  calculateValue (players) {
    this.setValue(players.filter(player => player.isFilled).length);
  }
}

export class SameClubRequirement extends Requirement {
  calculateValue (players) {
    const clubCounts = players
      .filter(player => player.isFilled)
      .reduce((acc, player) => {
        const clubId = player.data.club.ea_id;
        acc[clubId] = clubId in acc ? acc[clubId] + 1 : 1;

        return acc;
      }, {});

    this.setValue(Math.max(...Object.values(clubCounts)));
  }
}

export class SameLeagueRequirement extends Requirement {
  calculateValue (players) {
    const leagueCounts = players
      .filter(player => player.isFilled)
      .reduce((acc, player) => {
        const leagueId = player.data.league.ea_id;
        acc[leagueId] = leagueId in acc ? acc[leagueId] + 1 : 1;

        return acc;
      }, {});

    this.setValue(Math.max(...Object.values(leagueCounts)));
  }
}

export class SameNationRequirement extends Requirement {
  calculateValue (players) {
    const nationCounts = players
      .filter(player => player.isFilled)
      .reduce((acc, player) => {
        const nationId = player.data.nation.ea_id;
        acc[nationId] = nationId in acc ? acc[nationId] + 1 : 1;

        return acc;
      }, {});

    this.setValue(Math.max(...Object.values(nationCounts)));
  }
}

export class UniqueClubRequirement extends Requirement {
  calculateValue (players) {
    const uniqueClubs = players
      .filter(player => player.isFilled)
      .reduce((acc, player) => {
        const clubId = player.data.club.ea_id;

        if (acc.includes(clubId) === false) {
          acc.push(clubId);
        }

        return acc;
      }, []).length;

    this.setValue(uniqueClubs);
  }
}

export class UniqueLeagueRequirement extends Requirement {
  calculateValue (players) {
    const uniqueLeagues = players
      .filter(player => player.isFilled)
      .reduce((acc, player) => {
        const leagueId = player.data.league.ea_id;

        if (acc.includes(leagueId) === false) {
          acc.push(leagueId);
        }

        return acc;
      }, []).length;

    this.setValue(uniqueLeagues);
  }
}

export class UniqueNationRequirement extends Requirement {
  calculateValue (players) {
    const uniqueNations = players
      .filter(player => player.isFilled)
      .reduce((acc, player) => {
        const nationId = player.data.nation.ea_id;

        if (acc.includes(nationId) === false) {
          acc.push(nationId);
        }

        return acc;
      }, []).length;

    this.setValue(uniqueNations);
  }
}
