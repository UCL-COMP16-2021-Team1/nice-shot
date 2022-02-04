// Example code from THREE documentation on GTLFLoader

/**
 * Disclaimer about browser compatibility:
 * "GLTFLoader relies on ES6 Promises, which are not supported in IE11. 
 * To use the loader in IE11, you must include a polyfill providing 
 * a Promise replacement."
 */
const loader = new GTLFLoader();
loader.load(
    "resource_link", // resource URL. to be updated once .gtlf files are ready
    function (gtlf){
        scene.add(gtlf.scene);
        gtlf.animations;
        gtlf.scene;
        gtlf.cameras;
        gtlf.asset;
    },
    function (xhr) {
        console.log((xhr.loaded/xhr.total * 100) + "%loaded");
    },
    function (error){
        console.log("An error happened");
    }
)
renderer.outputEncoding = THREE.sRGBEncoding;
