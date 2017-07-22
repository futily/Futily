const path = require('path')

module.exports = [
  require('postcss-easy-import'),
  require('postcss-sassy-mixins'),
  require('postcss-conditionals'),
  require('postcss-apply'),
  require('postcss-nested'),
  require('postcss-functions')({
    glob: path.join(
      __dirname,
      '../../futily',
      'assets',
      'css',
      'helpers',
      'functions',
      '*.js'
    )
  }),

  require('postcss-custom-properties'),
  require('postcss-custom-media'),
  require('postcss-media-minmax'),
  require('postcss-custom-selectors'),
  // Niceties
  require('postcss-assets')({
    basePath: 'futily/assets/',
    loadPaths: ['fonts/', 'img/'],
    baseUrl: '/static/'
  }),
  require('postcss-inline-svg')({
    path: 'futily/assets/svg/'
  }),
  require('postcss-brand-colors'),
  require('postcss-property-lookup'),
  require('postcss-lh')({
    rhythmUnit: 'vr'
  }),
  require('postcss-pxtorem'),
  require('postcss-will-change'),
  require('postcss-font-awesome'),
  require('postcss-round-subpixels'),
  require('postcss-calc'),
  require('postcss-hexrgba'),
  require('autoprefixer')
]
