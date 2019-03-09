const path                    = require('path'),
      CleanWebpackPlugin      = require('clean-webpack-plugin'),
      MiniCssExtractPlugin    = require('mini-css-extract-plugin'),
      nodeSassMagicImporter   = require('node-sass-magic-importer'),
      {VueLoaderPlugin}       = require('vue-loader'),
      OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin'),
      UglifyJsPlugin          = require('uglifyjs-webpack-plugin'),
      env                     = process.env.NODE_ENV,
      sourceMap               = env === 'development',
      minify                  = env === 'production'

const config = {
    mode:         env,
    target:       'web',
    entry:        {
        app:   ['./app/static/js/app.js',
                './app/static/scss/app.scss'],
        admin: ['./app/static/js/admin.js',
                './app/static/scss/admin.scss'],
        error: ['./app/static/scss/error.scss']
    },
    output:       {
        path:     path.resolve(__dirname, 'app/static/dist'),
        filename: 'js/[name].js'
    },
    optimization: {},
    resolve:      {
        alias:      {
            'vue$': 'vue/dist/vue.esm.js'
        },
        extensions: ['*', '.js', '.vue', '.json'],
        modules:    ['./node_modules',
                     './app/static/js/modules',
                     './app/static/js/components']
    },
    stats:        {
        colors: true
    },
    devtool:      sourceMap ? 'cheap-module-eval-source-map' : undefined,
    module:       {
        rules: [
            {
                test:    /\.m?js$/,
                exclude: /node_modules/,
                loader:  'babel-loader'
            },
            {
                test:    /\.vue$/,
                exclude: /node_modules/,
                loader:  'vue-loader'
            },
            {
                test: /\.(scss|sass|css)$/i,
                use:  [{loader: MiniCssExtractPlugin.loader, options: {sourceMap}},
                       {loader: 'css-loader', options: {sourceMap}},
                       {loader: 'postcss-loader', options: {sourceMap}},
                       'resolve-url-loader',
                       {loader: 'sass-loader', options: {sourceMap, importer: nodeSassMagicImporter()}},]
            },
            {
                test: /\.(woff(2)?|ttf|eot|svg)(\?v=\d+\.\d+\.\d+)?$/,
                use:  [{
                    loader:  'file-loader',
                    options: {
                        name:       '[name].[ext]',
                        outputPath: 'fonts/',
                        publicPath: '/static/dist/fonts/',
                    }
                }]
            }
        ]
    },
    plugins:      [
        new VueLoaderPlugin(),
        new CleanWebpackPlugin(['./app/static/dist']),
        new MiniCssExtractPlugin({filename: 'css/[name].css'})
    ]
}


if (minify) {
    config.optimization.minimizer = [
        new OptimizeCSSAssetsPlugin(),
        new UglifyJsPlugin({
                               cache:    true,
                               parallel: true,
                           }),
    ]
}

module.exports = config