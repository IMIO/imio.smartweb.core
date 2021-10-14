const path = require("path");

const { CleanWebpackPlugin } = require("clean-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const PlonePlugin = require("./webpackPlonePlugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const JsonMinimizerPlugin = require("json-minimizer-webpack-plugin");
const TerserPlugin = require("terser-webpack-plugin");

const PLONE_SITE_PATH = process.env.PLONE_SITE_PATH ? process.env.PLONE_SITE_PATH : "/Plone5";
const BUNDLE_NAME = "++plone++imio.smartweb.webcomponents";
const BUNDLE_PREFIX = "plone.bundles/imio.smartweb.webcomponents";

module.exports = (env, argv) => {
    const mode = argv.mode ? argv.mode : "development";
    return {
        mode: mode,
        entry: "./index.js",
        output: {
            path: path.resolve(__dirname, "./build"),
            filename: "js/smartweb-webcomponents-compiled.js",
        },
        plugins: [
            mode === "production" && new CleanWebpackPlugin(),
            new MiniCssExtractPlugin({
                filename: "css/[name].css",
            }),
        ].filter(Boolean),
        module: {
            rules: [
                {
                    test: /\.(js|mjs|jsx|ts|tsx)$/,
                    use: {
                        loader: "babel-loader",
                        options: {
                            presets: ["@babel/preset-env"],
                        },
                    },
                },
                {
                    test: /\.s[ac]ss$/i,
                    use: [
                        // In production, creates CSS files
                        // In development serve CSS through JS 'with style-loader'
                        {
                            loader:
                                mode === "development"
                                    ? "style-loader"
                                    : MiniCssExtractPlugin.loader,
                        },
                        // Translates CSS into CommonJS
                        {
                            loader: "css-loader",
                            options: {
                                sourceMap: mode === "development",
                            },
                        },
                        // Use postcss to add vendor prefixes and various transforms to the css
                        {
                            loader: "postcss-loader",
                            options: {
                                sourceMap: mode === "development",
                            },
                        },
                        {
                            loader: "sass-loader",
                            options: {
                                sourceMap: mode === "development",
                            },
                        },
                    ],
                },
                {
                    test: /\.css$/i,
                    use: [
                        // In production, creates CSS files
                        // In development serve CSS through JS 'with style-loader'
                        {
                            loader:
                                mode === "development"
                                    ? "style-loader"
                                    : MiniCssExtractPlugin.loader,
                        },
                        // Translates CSS into CommonJS
                        {
                            loader: "css-loader",
                            options: {
                                sourceMap: mode === "development",
                            },
                        },
                    ],
                },
                {
                    test: /\.svg$/i,
                    issuer: /\.(js|mjs|jsx|ts|tsx)$/,
                    use: [
                        {
                            loader: "@svgr/webpack",
                        },
                    ],
                },
                {
                    test: /\.(png|jpg|gif|jpeg|svg)$/i,
                    loader: "file-loader",
                    options: {
                        name: "[name].[ext]",
                        outputPath: "assets",
                    },
                },
                {
                    test: /\.(eot|woff|woff2|ttf)([?]?.*)$/,
                    loader: "file-loader",
                    options: {
                        name: "[name].[ext]",
                        outputPath: "assets/fonts",
                    },
                },
            ],
        },
        resolve: {
            alias: {
                leaflet$: "leaflet/dist/leaflet",
            },
        },
        externals: {
            jquery: "jQuery",
        },
        optimization: {
            usedExports: true,
            minimizer: [
                new CssMinimizerPlugin(),
                new JsonMinimizerPlugin(),
                // new TerserPlugin({
                //     parallel: true,
                // }),
            ],
        },
        performance: {
            maxAssetSize: 750 * 1024,
            maxEntrypointSize: 750 * 1024,
        },
        devServer: {
            port: 3000,
            hot: true,
            watchFiles: {
                paths: ["./../**/*.pt"], // Watch for .pt file change
            },
            // Proxy everything to the Plone Backend EXCEPT our bundle as
            // Webpack Dev Server will serve it.
            proxy: [
                {
                    context: ["/**", `!${PLONE_SITE_PATH}/${BUNDLE_NAME}/**`],
                    target: "http://localhost:8080",
                },
                {
                    context: [`${PLONE_SITE_PATH}/${BUNDLE_NAME}/**`],
                    target: "http://localhost:3000",
                    pathRewrite: function (path) {
                        // We need to rewrite the path as Plone add some crap timestamp
                        // to it and doesn't provide a way of disabling it.
                        if (path.includes("++unique++")) {
                            const reg = /\/\+\+unique\+\+[^/]+/; // Strip ++unique++ part
                            path = path.replace(reg, "");
                        }
                        path = path.replace(`${PLONE_SITE_PATH}/${BUNDLE_NAME}/`, "");
                        return path;
                    },
                },
            ],
        },
    };
};
