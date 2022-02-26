import * as three from 'three';

import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader.js';
import {OrbitControls} from 'three/examples/jsm/controls/OrbitControls';

let scene, renderer, camera;

function initCamera(){
    camera = new THREE.PerspectiveCamera( // may want to try other type of projection
        75,
        window.innerWidth / window.innerHeight,
        0.1,
        1000
    );
    camera.position.z = -2; // any simpler way of determininig the positions?
    camera.position.y = 1.5;
    camera.position.x = 0;
    camera.lookAt(0,1,0);
}

function initScene(){
    scene = new THREE.Scene();
    scene.add(new THREE.AxesHelper(5));
    scene.background = new THREE.Color(0xfe0000) // green
    // can i return multiple items in javascript?
}

function initLighting(){
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
    scene.add(ambientLight);
    const light = new THREE.SpotLight();
    light.position.set(5,5,5);
    scene.add(light);
}

function initControls(){
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
}

function loadModel(){
    const modelLoader = new GLTFLoader();
    modelLoader.load(
        'Soldier.glb',
        function(gltf){
            scene.add(gltf.scene);
        },
        undefined,
        function error(e){
            console.error(e);
        }
    );
}

function initWindow(){
    window.addEventListener('resize', onWindowResize, false);
    function onWindowResize(){
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.render( scene, camera );
    }
}

function init(){
    const container = document.getElementById('3DImage');
    document.body.appendChild(container);

    initCamera();

    initScene();

    initLighting();

    initControls();

    loadModel();

    initWindow();

}

init();

renderer.render( scene, camera );
