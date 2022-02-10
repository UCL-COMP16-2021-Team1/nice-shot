import _ from 'lodash';
import * as THREE from 'three';

function component() {
    const element = document.createElement('div');
  
    // Lodash, now imported by this script
    element.innerHTML = _.join(['Hello', 'webpack'], ' ');
  
    return element;
  }
  
  document.body.appendChild(component());

import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader.js';
//import {3DMLoader} from 'https://cdn.jsdelivr.net/npm/three@0.137.5/examples/jsm/loaders/3DMLoader.min.js';

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);

const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);


const loader = new GLTFLoader();

loader.load('scene.gltf', function(gtlf){
    scene.add(gtlf.scene);
}, undefined, function(error){
    console.error(error);
});



camera.position.z = 5;
renderer.render( scene, camera );