const path                    = require('path'),
      outputPath              = path.resolve(__dirname, 'app/static/dist'),
      CleanWebpackPlugin      = require('clean-webpack-plugin'),
      MiniCssExtractPlugin    = require('mini-css-extract-plugin'),
      Fiber                   = require('fibers'),
      {VueLoaderPlugin}       = require('vue-loader'),
      OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin'),
      UglifyJsPlugin          = require('uglifyjs-webpack-plugin'),
      env                     = process.env.NODE_ENV,
      npm_config_argv         = JSON.parse(process.env.npm_config_argv),
      isWatch                 = npm_config_argv.remain.some(el => el.startsWith("--watch")),
      sourceMap               = env !== 'production',
      production              = env === 'production',
      webpack                 = require('webpack')

const config = {
    mode:         env,
    target:       'web',
    entry:        {
        frontend: ['./app/static/js/frontend/frontend.js',
                   './app/static/scss/frontend/frontend.scss'],
        backend:  ['./app/static/js/backend/backend.js',
                   './app/static/scss/backend/backend.scss']
    },
    output:       {
        path:     outputPath,
        filename: 'js/[name].js'
    },
    optimization: {},
    resolve:      {
        alias:      {
            'vue$': 'vue/dist/vue.esm.js'
        },
        extensions: ['*', '.js', '.vue', '.json'],
        modules:    ['./node_modules',
                     './app/static/js/frontend/components',
                     './app/static/js/frontend/pages',
                     './app/static/js/backend/components',
                     './app/static/js/backend/pages']
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
                test: /\.(sa|sc|c)ss$/i,
                use:  [
                    {
                        loader:  MiniCssExtractPlugin.loader,
                        options: {sourceMap}
                    },
                    {
                        loader:  'css-loader',
                        options: {
                            sourceMap,
                            importLoaders: 2
                        }
                    },
                    {loader: 'postcss-loader', options: {sourceMap}},
                    'resolve-url-loader',
                    {
                        loader:  'sass-loader',
                        options: {
                            sourceMap,
                            implementation: require("sass"),
                            fiber:          Fiber,
                            includePaths:   [path.resolve(__dirname, 'app/static/scss')]
                        }
                    },]
            },
            {
                test: /\.(woff(2)?|ttf|eot|svg)(\?v=\d+\.\d+\.\d+)?$/,
                use:  [{
                    loader:  'file-loader',
                    options: {
                        name:       "[name].[ext]",
                        outputPath: "fonts/",
                        publicPath: "/static/dist/fonts/",
                    }
                }]
            },
            {
                test:    /\.(ico|jpe?g|png|gif|webp)(\?.*)?$/,
                loader:  "file-loader",
                options: {
                    name:       "[name].[ext]",
                    outputPath: "images/",
                    publicPath: "/static/dist/images/",
                }
            }
        ]
    },
    plugins:      [
        new webpack.ProgressPlugin(),
        new VueLoaderPlugin(),
        new CleanWebpackPlugin({cleanStaleWebpackAssets: !isWatch}),
        new MiniCssExtractPlugin({
                                     path:          outputPath + '/css',
                                     filename:      'css/[name].css',
                                     chunkFilename: '[id].css'
                                 }),
        new webpack.NormalModuleReplacementPlugin(/element-ui[\/\\]lib[\/\\]locale[\/\\]lang[\/\\]zh-CN/,
                                                  'element-ui/lib/locale/lang/en')
    ]
}


if (production) {
    config.optimization.minimizer = [
        new OptimizeCSSAssetsPlugin(),
        new UglifyJsPlugin({
                               cache:    true,
                               parallel: true,
                           }),
    ]
}

module.exports = config