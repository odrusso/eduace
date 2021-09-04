// eslint-disable-next-line no-undef,@typescript-eslint/no-var-requires
const path = require('path');
// eslint-disable-next-line no-undef,@typescript-eslint/no-var-requires
const HtmlWebPackPlugin = require('html-webpack-plugin');

// eslint-disable-next-line no-undef
module.exports = {
    entry: "./src/index.tsx",
    output: {
        path: path.resolve(__dirname, 'build'),
        filename: 'bundle.js',
        publicPath: '/'
    },
    resolve: {
        extensions: [".jsx", ".js", ".tsx", "ts"],
        modules: [path.join(__dirname, 'src'), 'node_modules'],
        alias: {
            react: path.join(__dirname, 'node_modules', 'react'),
        },
    },
    module: {
        rules: [
            {
                test: /\.(js|jsx|ts|tsx)$/,
                exclude: /node_modules/,
                use: {
                    loader: 'ts-loader',
                },
            },
            {
                test: /\.css$/,
                use: [
                    {
                        loader: 'style-loader',
                    },
                    {
                        loader: 'css-loader',
                    },
                ],
            },
            {
                test: /\.ttf$/,
                loader: 'file-loader',
                options: {
                    name: '[name].[ext]',
                    outputPath: 'fonts/'
                }
            },
            {
                enforce: "pre",
                test: /\.js$/,
                exclude: /node_modules/,
                loader: "source-map-loader"
            }
        ],
    },
    devServer: {
        historyApiFallback: {
            index: '/'
        }
    },
    plugins: [
        new HtmlWebPackPlugin({
            template: './src/index.html',
            // favicon: './src/favicon.svg'
        })
    ],
    devtool: "source-map"
};