// Example code from THREE documentation on GTLFLoader

/**
 * Disclaimer about browser compatibility:
 * "GLTFLoader relies on ES6 Promises, which are not supported in IE11. 
 * To use the loader in IE11, you must include a polyfill providing 
 * a Promise replacement."
 */

import * as THREE from 'https://cdn.skypack.dev/pin/three@v0.137.5-HJEdoVYPhjkiJWkt6XIa/mode=imports/optimized/three.js';

//import {GLTFLoader} from 'https://cdn.jsdelivr.net/npm/three@0.137.5/examples/jsm/loaders/GLTFLoader.js';
//import {3DMLoader} from 'https://cdn.jsdelivr.net/npm/three@0.137.5/examples/jsm/loaders/3DMLoader.min.js';

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);

const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);


const loader = new GLTFLoader();

loader.load('scene.gtlf', function(gtlf){
    scene.add(gtlf.scene);
}, undefined, function(error){
    console.error(error);
});



camera.position.z = 5;
renderer.render( scene, camera );