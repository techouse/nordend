const merge  = require('webpack-merge'),
      common = require('./webpack.common.js')

module.exports = merge(common, {
    mode:    'development',
    devtool: 'inline-source-map',
    entry:   {
        app: ['./kilc/static/js/app.js',
              './kilc/static/scss/app.scss']
    }
})