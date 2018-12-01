const merge        = require('webpack-merge'),
      MinifyPlugin = require('babel-minify-webpack-plugin'),
      common       = require('./webpack.common.js')

module.exports = merge(common, {
    mode:    'production',
    plugins: [
        new MinifyPlugin()
    ],
    entry:   {
        app: ['babel-polyfill',
              './app/static/js/app.js',
              './app/static/scss/app.scss']
    },
    resolve: {
        modules: ['./node_modules',
                  './app/static/js/modules']
    }
})