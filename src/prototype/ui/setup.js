// Setup
$.ajaxSetup({
    async: false
});
let shots, shotCount;
$.getJSON("data/test_shot.json", function (data) {
    shots = data.shots;
    shotCount = shots.length;
}).fail(function () {
    console.log("The JSON file could not be loaded.");
});