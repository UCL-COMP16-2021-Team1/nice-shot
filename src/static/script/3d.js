// setup scene
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.z = 2;

const renderer = new THREE.WebGLRenderer({
	antialias: true,
});
renderer.setSize(window.innerWidth, 800);//window.innerWidth, window.innerHeight);
let container = document.getElementById("reconstruction");
container.appendChild(renderer.domElement);

const controls = new THREE.OrbitControls(camera, renderer.domElement);

const gridHelper = new THREE.GridHelper(10, 10);
scene.add(gridHelper);

const clock = new THREE.Clock();

// create joints
function create_joint() {
	const geometry = new THREE.SphereGeometry(0.01, 32, 16);
	const material = new THREE.MeshBasicMaterial({color: 0xff0000});
	const joint = new THREE.Mesh(geometry, material);
	return joint;
};

function update_joint_position(joint, keyframes, idx) {
	floor = Math.floor(idx);
	ceil = Math.ceil(idx);
	t = ceil - idx;
	joint.position.x = (1-t) * keyframes[ceil][0] + t * keyframes[floor][0];
	joint.position.y = -((1-t) * keyframes[ceil][1] + t * keyframes[floor][1]) + 0.7;
	joint.position.z = (1-t) * keyframes[ceil][2] + t * keyframes[floor][2];
};

function create_line_between_joints(j0, j1) {
	const geometry = new THREE.BufferGeometry().setFromPoints([j0.position, j1.position]);
	const material = new THREE.LineBasicMaterial({color: 0x00ffff});
	const line = new THREE.Line(geometry, material);
	return line;
};

const head = create_joint();
const neck = create_joint();
const left_shoulder = create_joint();
const right_shoulder = create_joint();
const torso = create_joint();
const left_hip = create_joint();
const right_hip = create_joint();
const left_elbow = create_joint();
const right_elbow = create_joint();
const left_wrist = create_joint();
const right_wrist = create_joint();
const left_knee = create_joint();
const right_knee = create_joint();
const left_foot = create_joint();
const right_foot = create_joint();

scene.add(head);
scene.add(neck);
scene.add(left_shoulder);
scene.add(right_shoulder);
scene.add(torso)
scene.add(left_hip);
scene.add(right_hip);
scene.add(left_elbow);
scene.add(right_elbow);
scene.add(left_wrist);
scene.add(right_wrist);
scene.add(left_knee);
scene.add(right_knee);
scene.add(left_foot);
scene.add(right_foot);

// create shot trail
var shot_trail_points = [];
for (let i = 0; i < shot.world_keyframes.left_wrist.length; i++) {
	var p = shot.world_keyframes.left_wrist[i]
	shot_trail_points.push(new THREE.Vector3(p[0], -p[1]+0.7, p[2]));
}
const curve = new THREE.CatmullRomCurve3(shot_trail_points);
const points = curve.getPoints(100);
const geometry = new THREE.BufferGeometry().setFromPoints(points);
const material = new THREE.LineBasicMaterial( { color: 0xff00ff } );
const shot_trail = new THREE.Line( geometry, material );
shot_trail.visible = false;
scene.add(shot_trail)

var shot_trail_options = {
	hide: function() {
		shot_trail.visible = false;
	},
	show: function() {
		shot_trail.visible = true;
	}
}

// animate joints and connections
const frame_count = shot.world_keyframes.head.length;
var frame_idx = 0;
var anim_options = {	// options for GUI
	paused: false,
	speed: 100,
	pause: function() {
		this.paused = true;
	},
	play: function() {
		this.paused = false;
	},
	step_size: 1,
	step_forward: function() {
		frame_idx += this.step_size;
		if (frame_idx > frame_count - 1) {
			frame_idx -= (frame_count - 1);
		}
	},
	step_backward: function() {
		frame_idx -= this.step_size;
		if (frame_idx < 0) {
			frame_idx = (frame_count - 1) - Math.abs(frame_idx);
		}
	}
};

var joint_lines = [];
function animate() {
	requestAnimationFrame(animate);

	update_joint_position(head, shot.world_keyframes.head, frame_idx)
	update_joint_position(neck, shot.world_keyframes.neck, frame_idx)
	update_joint_position(left_shoulder, shot.world_keyframes.left_shoulder, frame_idx)
	update_joint_position(right_shoulder, shot.world_keyframes.right_shoulder, frame_idx)
	update_joint_position(torso, shot.world_keyframes.torso, frame_idx)
	update_joint_position(left_hip, shot.world_keyframes.left_hip, frame_idx)
	update_joint_position(right_hip, shot.world_keyframes.right_hip, frame_idx)
	update_joint_position(left_elbow, shot.world_keyframes.left_elbow, frame_idx)
	update_joint_position(right_elbow, shot.world_keyframes.right_elbow, frame_idx)
	update_joint_position(left_wrist, shot.world_keyframes.left_wrist, frame_idx)
	update_joint_position(right_wrist, shot.world_keyframes.right_wrist, frame_idx)
	update_joint_position(left_knee, shot.world_keyframes.left_knee, frame_idx)
	update_joint_position(right_knee, shot.world_keyframes.right_knee, frame_idx)
	update_joint_position(left_foot, shot.world_keyframes.left_foot, frame_idx)
	update_joint_position(right_foot, shot.world_keyframes.right_foot, frame_idx)

	while (joint_lines.length > 0) {
		line = joint_lines.pop()
		scene.remove(line)
		line.geometry.dispose()
		line.material.dispose()
	}

	joint_lines.push(create_line_between_joints(head, neck));
	joint_lines.push(create_line_between_joints(left_shoulder, neck));
	joint_lines.push(create_line_between_joints(right_shoulder, neck));
	joint_lines.push(create_line_between_joints(torso, neck));
	joint_lines.push(create_line_between_joints(torso, left_hip));
	joint_lines.push(create_line_between_joints(torso, right_hip));
	joint_lines.push(create_line_between_joints(left_shoulder, left_elbow));
	joint_lines.push(create_line_between_joints(right_shoulder, right_elbow));
	joint_lines.push(create_line_between_joints(left_elbow, left_wrist))
	joint_lines.push(create_line_between_joints(right_elbow, right_wrist));
	joint_lines.push(create_line_between_joints(left_hip, left_knee));
	joint_lines.push(create_line_between_joints(right_hip, right_knee));
	joint_lines.push(create_line_between_joints(left_knee, left_foot));
	joint_lines.push(create_line_between_joints(right_knee, right_foot));

	for (let i = 0; i < joint_lines.length; i++) {
		scene.add(joint_lines[i]);
	}

	if (!anim_options.paused) {
		frame_idx += anim_options.speed * clock.getDelta();
		if (frame_idx > frame_count - 1) {
			frame_idx = 0;
		}
	}
	renderer.render(scene, camera);
};

// setup GUI
var gui = new dat.GUI();

var anim = gui.addFolder(shot.classification);
anim.add(anim_options, 'speed', 0, 100).listen();
anim.add(anim_options, 'pause');
anim.add(anim_options, 'play');
anim.add(anim_options, 'step_size', 0, 10).listen();
anim.add(anim_options, 'step_forward');
anim.add(anim_options, 'step_backward');
anim.open();

var path = gui.addFolder('shot path');
path.add(shot_trail_options, 'show');
path.add(shot_trail_options, 'hide');
path.open();

animate();