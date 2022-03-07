import * as THREE from 'three';

import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';

let scene, renderer, camera;
let idleAction, walkAction, runAction;
//let idleWeight, walkWeight, runWeight;
let model;

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
camera.position.z = -2;
camera.position.y = 1.5;
camera.position.x = 0;
camera.lookAt(0,1,0);

// init renderer
renderer = new THREE.WebGLRenderer({antialiasing: true});
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.outputEncoding = THREE.sRGBEncoding;
container.appendChild(renderer.domElement);

// init scene
scene = new THREE.Scene();
scene.add(new THREE.AxesHelper(5));
scene.background = new THREE.Color(0xfe000);

/*const ambientLight = new THREE.AmbientLight( 0xffffff, 0.4 );
scene.add( ambientLight );*/

const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
scene.add(ambientLight);

const light = new THREE.SpotLight();
light.position.set(5,5,5);
scene.add(light);
/*
//const dirLight = new THREE.DirectionalLight( 0xefefff, 1.5 );
dirLight.position.set( 10, 10, 10 );
scene.add( dirLight );
*/

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;

// init loader
const modelLoader = new GLTFLoader();
modelLoader.load(
    'Soldier.glb',
    function(gltf){
    scene.add(gltf.scene);
    const animations = gltf.animations;

	mixer = new THREE.AnimationMixer( gltf.scene );

	idleAction = mixer.clipAction( animations[ 0 ] );
	walkAction = mixer.clipAction( animations[ 3 ] );
	runAction = mixer.clipAction( animations[ 1 ] );

	actions = [ idleAction, walkAction, runAction ];

	activateAllActions();

	animate();
    },
    undefined,
    function error(e){
        console.error(e);
    }
);

window.addEventListener('resize', onWindowResize, false);
function onWindowResize(){
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    render();
}

function activateAllActions() {

    setWeight( idleAction, settings[ 'modify idle weight' ] );
    setWeight( walkAction, settings[ 'modify walk weight' ] );
    setWeight( runAction, settings[ 'modify run weight' ] );

    actions.forEach( function ( action ) {
        action.play();
    });
}

function animate() {

    // Render loop

    requestAnimationFrame( animate );

    const idleWeight = idleAction.getEffectiveWeight();
    const walkWeight = walkAction.getEffectiveWeight();
    const runWeight = runAction.getEffectiveWeight();

    // Get the time elapsed since the last frame, used for mixer update (if not in single step mode)

    let mixerUpdateDelta = clock.getDelta();

    // If in single step mode, make one step and then do nothing (until the user clicks again)

    if ( singleStepMode ) {

        mixerUpdateDelta = sizeOfNextStep;
        sizeOfNextStep = 0;

    }

    // Update the animation mixer, the stats panel, and render this frame

    //mixer.update( mixerUpdateDelta );

    renderer.render( scene, camera );

}

/*function animate(){
    requestAnimationFrame(animate);
    controls.update();
    render();
}*/

function render(){
    renderer.render(scene, camera);
}

//animate();


//render();