const path = require('path');

function entrypath (string) {
    const dir = './src/ui/';
    return path.resolve(dir, string);
}

module.exports = {
    mode: 'development',
    entry: {
        index: entrypath('index.js'),
        print: entrypath('print.js'),
    },
    output: {
        filename: '[name].bundle.js',
        path: path.resolve(__dirname, 'dist'),
        clean: true,
    },
};

