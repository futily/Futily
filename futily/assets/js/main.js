import 'babel-polyfill'
import 'pepjs'
import './utils/class-list-polyfill'

import { externalLinks, iframeFix } from './utils'
import { FloatingLabel } from './forms'
import { PlayerFilterForm } from './players/list'
import { Follow } from './users/follow'
import {
  ComparePlayerSearch,
  HeaderPlayerSearch,
  SectionPlayerSearch,
  SettingsClubSearch,
  SettingsNationSearch,
  SettingsPlayerSearch
} from './search'

document.addEventListener('DOMContentLoaded', () => {
  externalLinks()

  if (document.querySelector('.js-UserFollow')) {
    new Follow({ el: document.querySelector('.js-UserFollow') })
  }

  if (document.querySelector('.js-PlayerFilter')) {
    const playerFilter = Object.create(PlayerFilterForm)
    playerFilter.init({ el: document.querySelector('.js-PlayerFilter') })
  }

  if (document.querySelector('.plyr-CardSelector')) {
    import('./players/detail').then(players => {
      new players.CardSelector()
    })
  }

  if (document.querySelector('.js-ObjectRating')) {
    import('./site/vote').then(vote => {
      new vote.Vote({ className: '.js-ObjectRating' })
    })
  }

  if (document.querySelector('.js-RPP')) {
    import('./players/detail').then(players => {
      new players.RPP()
    })
  }

  if (document.querySelector('.js-FloatingLabel')) {
    const labels = document.querySelectorAll('.js-FloatingLabel')

    Array.from(labels).map(label => {
      new FloatingLabel({ el: label })
    })
  }

  if (document.querySelector('.js-HeaderPlayerSearch')) {
    new HeaderPlayerSearch({ className: '.js-HeaderPlayerSearch' })
  }

  if (document.querySelector('.js-ComparePlayerSearch')) {
    new ComparePlayerSearch({ className: '.js-ComparePlayerSearch' })
  }

  if (document.querySelector('.js-SectionPlayerSearch')) {
    new SectionPlayerSearch({ className: '.js-SectionPlayerSearch' })
  }

  if (document.querySelector('.js-SettingsPlayerSearch')) {
    new SettingsPlayerSearch({ className: '.js-SettingsPlayerSearch' })
  }

  if (document.querySelector('.js-SettingsClubSearch')) {
    new SettingsClubSearch({ className: '.js-SettingsClubSearch' })
  }

  if (document.querySelector('.js-SettingsNationSearch')) {
    new SettingsNationSearch({ className: '.js-SettingsNationSearch' })
  }

  if (document.querySelector('.js-Builder')) {
    import('./squads').then(squads => {
      if (document.querySelector('.js-Builder-challenge')) {
        new squads.SquadChallenge({
          className: 'bld-Builder',
          isEditable: true
        })
      } else {
        new squads.SquadBuilder({ className: 'bld-Builder', isEditable: true })
      }
    })
  }

  if (document.querySelector('.js-Detail')) {
    import('./squads').then(squads => {
      new squads.SquadDetail({ className: 'bld-Builder' })
    })
  }

  // If the browser isn't Safari, don't do anything
  if (
    document.querySelector('iframe') &&
    window.navigator.userAgent.indexOf('Safari') > -1
  ) {
    iframeFix()
  }

  // If the device is iOS add a class to the body so we can do specific CSS for
  // it
  if (!!navigator.platform && /iPad|iPhone|iPod/.test(navigator.platform)) {
    const body = document.body || document.documentElement
    body.classList.add('is-iOS')
  }

  // This class is used for making the animation duration on CSS animations 0,
  // initially
  setTimeout(() => {
    document.body.classList.remove('util-Preload')
  }, 500)
})
