import 'babel-polyfill'
import 'pepjs'
import './utils/class-list-polyfill'

import Vue from 'vue'
import InstantSearch from 'vue-instantsearch'
import { map } from 'lodash'

import App from './vue/App'

import { externalLinks, iframeFix } from './utils'
import { FloatingLabel } from './forms'
import { CardSelector, RPP } from './players/detail'
import { PlayerFilterForm } from './players/list'
import { Follow } from './users/follow'
import {
  ComparePlayerSearch,
  HeaderPlayerSearch,
  SectionPlayerSearch
} from './search'

Vue.use(InstantSearch)

new Vue(App).$mount('#app')

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
    new CardSelector()
  }

  if (document.querySelector('.js-RPP')) {
    new RPP()
  }

  if (document.querySelector('.js-FloatingLabel')) {
    const labels = document.querySelectorAll('.js-FloatingLabel')

    map(labels, label => {
      new FloatingLabel({ el: label })
    })
  }

  if (document.querySelector('.onespacemedia-login')) {
    let scriptAdded = false
    const googleLoginButton = document.querySelector('.onespacemedia-login')
    const formEl = document.getElementById('google-plus')
    const atEl = document.getElementById('at')
    const codeEl = document.getElementById('code')

    googleLoginButton.addEventListener('click', () => {
      if (!scriptAdded) {
        const po = document.createElement('script')
        po.type = 'text/javascript'
        po.async = true
        po.src = 'https://apis.google.com/js/client:plusone.js'

        const s = document.getElementsByTagName('script')[0]
        s.parentNode.insertBefore(po, s)

        scriptAdded = true
      }
    })

    window.signInCallback = function signInCallback (result) {
      console.log(result)

      if (result['error']) {
        console.log(result['error'])
      } else {
        codeEl.value = result['code']
        atEl.value = result['at']
        formEl.submit()
      }
    }
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
