import 'babel-polyfill'
import 'pepjs'
import 'utils/class-list-polyfill'

import Vue from 'vue'

import App from './vue/App'

import { externalLinks, iframeFix } from './utils'
import { PlayerFilterForm } from './players/list'

new Vue(App).$mount('#app')

document.addEventListener('DOMContentLoaded', () => {
  externalLinks()

  if (document.querySelector('.js-PlayerFilter')) {
    const playerFilter = Object.create(PlayerFilterForm)
    playerFilter.init({ el: document.querySelector('.js-PlayerFilter') })
  }

  // If the browser isn't Safari, don't do anything
  if (
    document.querySelector('iframe') &&
    window.navigator.userAgent.indexOf('Safari') > -1
  ) {
    iframeFix()
  }

  // If the device is iOS add a class to the body so we can do specific CSS for it
  if (!!navigator.platform && /iPad|iPhone|iPod/.test(navigator.platform)) {
    const body = document.body || document.documentElement
    body.classList.add('is-iOS')
  }

  // This class is used for making the animation duration on CSS animations 0, initially
  setTimeout(() => {
    document.body.classList.remove('util-Preload')
  }, 500)
})
