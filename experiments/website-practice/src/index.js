import * as THREE from 'three';

import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader.js';

let scene, renderer, camera;

// Initialisation, based on https://github.com/mrdoob/three.js/blob/master/examples/webgl_animation_skinning_blending.html
// Guide used. https://sbcode.net/threejs/loaders-gltf/

// init container
const container = document.getElementById('container');
document.body.appendChild(container);

// init camera
camera = new THREE.PerspectiveCamera(
    75, 
    window.innerWidth / window.innerHeight, 
    0.1, 
    1000
);
camera.position.z = 2;
camera.position.y = 1;

// init renderer
renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
container.appendChild(renderer.domElement);

// init scene
scene = new THREE.Scene();
scene.add(new THREE.AxesHelper(5));
scene.background = new THREE.Color(0xfe000);

// init loader
const modelLoader = new GLTFLoader();
modelLoader.load(
    'Soldier.glb',
    function(gltf){
    scene.add(gltf.scene);
    },
    undefined,
    function error(e){
        console.error(e);
    });

window.addEventListener('resize', onWindowResize, false);
function onWindowResize(){
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    render();
}

function render(){
    renderer.render(scene, camera);
}

render();