const path = require('path');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const TerserPlugin = require("terser-webpack-plugin");


module.exports = {
    mode: 'development',
    entry: {
        view: './src/view.js',
        edit: './src/edit.js',
        swiperconfig: './src/swiper-config.js',

    },
    output: {
        filename: 'smartweb-[name]-compiled.js',
        path: path.resolve(__dirname, ''),
    },
    module: {
        rules: [
            {
                test: /\.less$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    'css-loader',
                    'less-loader'
                ],
            },
        ]
    },
    plugins: [
        new MiniCssExtractPlugin({
            filename: 'smartweb-[name]-compiled.css',
        }),
    ],
    optimization: {
        usedExports: true,
        minimize: true,
        minimizer: [
          new CssMinimizerPlugin(),
          new TerserPlugin()
        ],
      },
};