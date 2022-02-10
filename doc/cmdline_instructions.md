# Instructions for running the website with Node


## Install node.js
I use a mac so I used `brew install node`, I'm not sure about other operating systems.

## Initialise the npm development environment
In the area the website's code will be.  
```
npm init
```


## Install dependencies
- webpack (to bundle the javascript code):  
  ```
  npm install webpack webpack-cli --save
  ```  
- three:  
  ```
  npm install three --save
  ```  

N.B. Use `--save-dev` instead for development purposes.
(I also added the lodash library, but that was only for testing)

## Set directories
Create the **source** and **distribution** directories.  
The code snippet below from [Webpack](https://webpack.js.org/guides/getting-started/#basic-setup) illustrates this well.
```
  webpack-demo
  |- package.json
  |- package-lock.json
  |- webpack.config.js
  |- /dist
    |- index.html
  |- /src
    |- index.js
```

### Configure Webpack settings
(from `webpack.config.js`)
```
const path = require('path');

module.exports = {
  entry: './src/index.js',
  output: {
    filename: 'main.js',
    path: path.resolve(__dirname, 'dist'),
  },
};
```

## Bundle the code
In the current directory, run  
```
npx webpack --mode=development
```
The mode can be changed to `--mode=production` for publishing purposes.

## Run the server
Given you can use ` five-server`, in the `dist/` directory, run:
```
five-server . -p 8000     
```
The website should theoretically work.