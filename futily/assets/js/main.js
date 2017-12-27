import 'babel-polyfill';
import 'intersection-observer';
import 'pepjs';
import './utils/class-list-polyfill';

import { externalLinks, iframeFix } from './utils';
import { FloatingLabel } from './forms';
import { PlayerFilterForm } from './players/list';
import { Navigation } from './site';
import { Follow } from './users/follow';
import {
  ComparePlayerSearch,
  HeaderPlayerSearch,
  SectionPlayerSearch,
  SettingsClubSearch,
  SettingsNationSearch,
  SettingsPlayerSearch,
} from './search';

document.addEventListener('DOMContentLoaded', () => {
  externalLinks();
  new Navigation();

  if (document.querySelector('.js-Comments')) {
    import('./comments').then(comments => {
      new comments.default( // eslint-disable-line
        JSON.parse(
          document.querySelector('.js-Comments').dataset.commentsConfig
        )
      );
    });
  }

  const builderEl = document.getElementById('js-Builder');
  if (builderEl) {
    import('./builder').then(builder => {
      const formation = builderEl.dataset.formation;
      const initial = builderEl.dataset.initial
        ? JSON.parse(builderEl.dataset.initial).map(([_, str]) => [
          _,
          JSON.parse(str),
        ])
        : [];
      const isEditable = builderEl.dataset.editable === 'true';
      const isSbc = builderEl.dataset.isSbc === 'true';
      const page = Number(builderEl.dataset.page);
      const awards = builderEl.dataset.awards
        ? JSON.parse(builderEl.dataset.awards).map(i => JSON.parse(i))
        : undefined;
      const requirements = builderEl.dataset.requirements
        ? JSON.parse(builderEl.dataset.requirements).map(i => {
          const json = JSON.parse(i);
          json['passed'] = false;

          return json;
        })
        : undefined;
      const saveUrl = builderEl.dataset.saveUrl;
      const sbcId = Number(builderEl.dataset.sbcId);
      const share = JSON.parse(builderEl.dataset.share);
      const title = builderEl.dataset.title;
      const user = JSON.parse(builderEl.dataset.user);

      builder.default({
        // eslint-disable-line
        awards,
        formation,
        initial,
        isEditable,
        isSbc,
        page,
        requirements,
        saveUrl,
        sbcId,
        share,
        title,
        user,
      });
    });
  }

  if (document.querySelector('.js-UserFollow')) {
    new Follow({ el: document.querySelector('.js-UserFollow') });
  }

  if (document.querySelector('.js-PlayerFilter')) {
    const playerFilter = Object.create(PlayerFilterForm);
    playerFilter.init({ el: document.querySelector('.js-PlayerFilter') });
  }

  if (document.querySelector('.plyr-CardSelector')) {
    import('./players/detail').then(players => {
      new players.CardSelector();
    });
  }

  if (document.querySelector('.js-ObjectRating')) {
    import('./site/vote').then(vote => {
      new vote.Vote({ className: '.js-ObjectRating' });
    });
  }

  if (document.querySelector('.js-RPP')) {
    import('./players/detail').then(players => {
      new players.RPP();

      const bars = document.querySelectorAll('.plyr-StatGroup_Bar');
      const callback = (entries, observer) => {
        Array.from(entries).forEach((entry, index) => {
          if (entry.isIntersecting) {
            window.setTimeout(() => {
              entry.target.classList.add('plyr-StatGroup_Bar-active');
              observer.unobserve(entry.target);
            }, 150 * index);
          }
        });
      };
      /* eslint-disable compat/compat */
      const observer = new IntersectionObserver(callback, {
        threshold: 0.2,
      });
      Array.from(bars).forEach(image => observer.observe(image));
    });
  }

  if (document.querySelector('.js-HeaderPlayerSearch')) {
    new HeaderPlayerSearch({ className: '.js-HeaderPlayerSearch' });
  }

  if (document.querySelector('.js-ComparePlayerSearch')) {
    new ComparePlayerSearch({ className: '.js-ComparePlayerSearch' });
  }

  if (document.querySelector('.js-SectionPlayerSearch')) {
    new SectionPlayerSearch({ className: '.js-SectionPlayerSearch' });
  }

  if (document.querySelector('.js-SettingsPlayerSearch')) {
    new SettingsPlayerSearch({ className: '.js-SettingsPlayerSearch' });
  }

  if (document.querySelector('.js-SettingsClubSearch')) {
    new SettingsClubSearch({ className: '.js-SettingsClubSearch' });
  }

  if (document.querySelector('.js-SettingsNationSearch')) {
    new SettingsNationSearch({ className: '.js-SettingsNationSearch' });
  }

  if (document.querySelector('.js-Builder')) {
    import('./squads').then(squads => {
      if (document.querySelector('.js-Builder-challenge')) {
        new squads.SquadChallenge({
          className: 'bld-Builder',
          isEditable: true,
        });
      }
    });
  }

  if (document.querySelector('.js-Detail')) {
    import('./squads').then(squads => {
      new squads.SquadDetail({ className: 'bld-Builder' });
    });
  }

  if (document.querySelector('.js-FloatingLabel')) {
    const labels = document.querySelectorAll('.js-FloatingLabel');

    Array.from(labels).map(label => {
      new FloatingLabel({ el: label });
    });
  }

  // If the browser isn't Safari, don't do anything
  if (
    document.querySelector('iframe') &&
    window.navigator.userAgent.indexOf('Safari') > -1
  ) {
    iframeFix();
  }

  // If the device is iOS add a class to the body so we can do specific CSS for
  // it
  if (!!navigator.platform && /iPad|iPhone|iPod/.test(navigator.platform)) {
    const body = document.body || document.documentElement;
    body.classList.add('is-iOS');
  }

  // This class is used for making the animation duration on CSS animations 0,
  // initially
  setTimeout(() => {
    document.body.classList.remove('util-Preload');
  }, 500);
});
