const merge  = require('webpack-merge'),
      common = require('./webpack.common.js')

module.exports = merge(common, {
    mode:    'development',
    devtool: 'inline-source-map',
    entry:   {
        app: ['./app/static/js/app.js',
              './app/static/scss/app.scss']
    }
})