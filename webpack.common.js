const path                 = require('path'),
      CleanWebpackPlugin   = require('clean-webpack-plugin'),
      MiniCssExtractPlugin = require("mini-css-extract-plugin")

module.exports = {
    target:  'web',
    output:  {
        path:     path.resolve(__dirname, 'app/static/dist'),
        filename: '[name].js'
    },
    resolve: {
        modules: ['./app/static/js/modules']
    },
    stats:   {
        colors: true
    },
    module:  {
        rules: [
            {
                test:    /\.js$/,
                exclude: /node_modules/,
                use:     {
                    loader: 'babel-loader'
                }
            },
            {
                test: /\.scss$/,
                use:  ['style-loader', MiniCssExtractPlugin.loader, 'css-loader', 'postcss-loader', 'sass-loader']
            }
        ]
    },
    plugins: [
        new CleanWebpackPlugin(['./app/static/dist']),
        new MiniCssExtractPlugin({filename: '[name].css'}),
    ]
}