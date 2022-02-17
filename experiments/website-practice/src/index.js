import * as THREE from 'three';

import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader.js';

let scene, renderer, camera;
let model;

// Initialisation, based on https://github.com/mrdoob/three.js/blob/master/examples/webgl_animation_skinning_blending.html

const container = document.getElementById('container');
document.body.appendChild(container);

camera = new THREE.PerspectiveCamera(45, window.innerHeight / window.innerHeight, 1, 1000);
camera.position.set(1,2,-3);
camera.lookAt(0,1,0);

scene = new THREE.Scene();
scene.background = new THREE.Color(0xa0a0a0);

const loader = new GLTFLoader();
loader.load('scifi_girl_v.01/scene.gltf', function(gltf){
    model = gltf.scene;
    scene.add(model);

}, 
undefined, 
function(e){
    console.error(e);
});

renderer = new THREE.WebGLRenderer({antialias:true});
renderer.setPixelRatio(window.devicePixelRatio);
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.outputEncoding = THREE.sRGBEncoding;
//renderer.shadowMap.enabled = true;
container.appendChild(renderer.domElement);
renderer.render(scene, camera);

/*

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);

const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);


const loader = new GLTFLoader();

loader.load(
    'scifi_girl_v.01/scene.gltf',
    function(gltf) {
        scene.add(gltf.scene);
        gltf.animations;
        gltf.scene;
        gltf.scenes;
        gltf.cameras;
        gltf.asset;
    },
    function (xhr) {
        console.log((xhr.loaded/xhr.total*100) + '% loaded');
    },
    function (error){
        console.log(error);
    }
);

camera.position.z = 5;
renderer.render( scene, camera );*/