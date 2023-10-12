const path = require("path");

const { CleanWebpackPlugin } = require("clean-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const JsonMinimizerPlugin = require("json-minimizer-webpack-plugin");
const TerserPlugin = require("terser-webpack-plugin");

const BUNDLE_NAME = "++plone++imio.smartweb.webcomponents";

module.exports = (env, argv) => {
    const mode = argv.mode ? argv.mode : "development";
    return {
        mode: mode,
        entry: ["core-js/stable", path.resolve(__dirname, "./src/index.jsx")],
        output: {
            path: path.resolve(__dirname, "./build"),
            filename: "js/smartweb-webcomponents-compiled.js",
        },
        plugins: [
            mode === "production" && new CleanWebpackPlugin(),
            new MiniCssExtractPlugin({
                filename: "css/smartweb-webcomponents-compiled.css",
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
                    // Use @svgr/webpack to import svg directly in .js files
                    test: /\.svg$/i,
                    issuer: /\.(js|mjs|jsx|ts|tsx)$/,
                    loader: "@svgr/webpack",
                },
                {
                    // Use file-loader to import img files in other files
                    test: /\.(png|jpg|gif|jpeg|svg)$/i,
                    loader: "file-loader",
                    options: {
                        name: "[name].[hash].[ext]",
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
            extensions: [".ts", ".js", ".tsx", ".jsx"], // Allow to import .jsx file without adding ".jsx" at the end
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
                new TerserPlugin({
                    parallel: true,
                }),
            ],
        },
        performance: {
            maxAssetSize: 2000 * 1024, // 2 Mo max for asset
            maxEntrypointSize: 750 * 1024, // 750 Ko max for entrypoint, if need more, use code-splitting with
        },
        devServer: {
            port: 2000,
            hot: true,
            watchFiles: {
                paths: ["./../**/*.pt"], // Also watch for .pt file change
            },
            // De-comment this when new resources registry is out.
            // Python webresource module adds a integrity token so we need to write to disk so it can be recomputed
            // devMiddleware: {
            //    writeToDisk: true,
            //},

            // Proxy everything to the Plone Backend EXCEPT our bundle as
            // Webpack Dev Server will serve it.
            proxy: [
                {
                    context: ["/**", `!**/${BUNDLE_NAME}/**`],
                    target: "http://localhost:8080",
                },
                {
                    context: [`**/${BUNDLE_NAME}/**`],
                    target: "http://localhost:2000",
                    pathRewrite: function (path) {
                        if (path.includes("++unique++")) {
                            // We need to rewrite the path as Plone 5 add some crap timestamp
                            // to it and doesn't provide a way of disabling it.
                            const reg = /\/\+\+unique\+\+[^/]+/; // Strip ++unique++ part
                            path = path.replace(reg, "");
                        }
                        path = path.split(BUNDLE_NAME)[1]; // Keep only the path after our bundle name
                        return path;
                    },
                },
            ],
        },
    };
};
