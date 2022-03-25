// setup scene
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.x = 2;
camera.position.z = 2;
camera.position.y = 2;

const renderer = new THREE.WebGLRenderer({
	antialias: true
});
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

const controls = new THREE.OrbitControls(camera, renderer.domElement);

const gridHelper = new THREE.GridHelper(10, 10);
scene.add(gridHelper);

const clock = new THREE.Clock();

function interpolate_joint_position(keyframes, idx) {
	floor = Math.floor(idx);
	ceil = Math.ceil(idx);
	t = ceil - idx;
	pos = new THREE.Vector3();
	pos.x = -((1-t) * keyframes[ceil][0] + t * keyframes[floor][0]);
	pos.y = -((1-t) * keyframes[ceil][1] + t * keyframes[floor][1]) + 0.7;
	pos.z = (1-t) * keyframes[ceil][2] + t * keyframes[floor][2];
	return pos;
};

function create_line_between_joints(j0, j1) {
	const geometry = new THREE.BufferGeometry().setFromPoints([j0, j1]);
	const material = new THREE.LineBasicMaterial({color: 0x00ffff});
	const line = new THREE.Line(geometry, material);
	return line;
};

// animate joints and connections
var shot;
var frame_count;
var frame_idx;
function set_shot() {
	shot = shots[shot_index];
	frame_count = shot.joint_frames.head.length;
	frame_idx = 0;
	$("#info").text("[" + shot_index + "] " + shot.classification);
}
set_shot();

const geometry = new THREE.SphereGeometry(0.01, 32, 16);
const material = new THREE.MeshBasicMaterial({color: 0xff0000});
const racket_indicator = new THREE.Mesh(geometry, material);
scene.add(racket_indicator);

// options for GUI
var anim_options = {
	paused: false,
	speed: 1,
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

var shot_options = {
	next_shot: function() {
		if (shot_index == shots.length - 1) {
			shot_index = 0;
		}
		else {
			shot_index++;
		}
		set_shot();
	},
	prev_shot: function() {
		if (shot_index == 0) {
			shot_index = shots.length - 1;
		}
		else {
			shot_index--;
		}
		set_shot();
	}
}

var joint_lines = [];
function animate() {
	requestAnimationFrame(animate);

	var head = interpolate_joint_position(shot.joint_frames.head, frame_idx);
	var neck = interpolate_joint_position(shot.joint_frames.neck, frame_idx);
	var left_shoulder = interpolate_joint_position(shot.joint_frames.left_shoulder, frame_idx);
	var right_shoulder = interpolate_joint_position(shot.joint_frames.right_shoulder, frame_idx);
	var torso = interpolate_joint_position(shot.joint_frames.torso, frame_idx);
	var left_hip = interpolate_joint_position(shot.joint_frames.left_hip, frame_idx);
	var right_hip = interpolate_joint_position(shot.joint_frames.right_hip, frame_idx);
	var left_elbow = interpolate_joint_position(shot.joint_frames.left_elbow, frame_idx);
	var right_elbow = interpolate_joint_position(shot.joint_frames.right_elbow, frame_idx);
	var left_wrist = interpolate_joint_position(shot.joint_frames.left_wrist, frame_idx);
	var right_wrist = interpolate_joint_position(shot.joint_frames.right_wrist, frame_idx);
	var left_knee = interpolate_joint_position(shot.joint_frames.left_knee, frame_idx);
	var right_knee = interpolate_joint_position(shot.joint_frames.right_knee, frame_idx);
	var left_foot = interpolate_joint_position(shot.joint_frames.left_foot, frame_idx);
	var right_foot = interpolate_joint_position(shot.joint_frames.right_foot, frame_idx);

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

	if (shot.hand == "left") {
		racket_indicator.position.x = left_wrist.x;
		racket_indicator.position.y = left_wrist.y;
		racket_indicator.position.z = left_wrist.z;
	}
	else {
		racket_indicator.position.x = right_wrist.x;
		racket_indicator.position.y = right_wrist.y;
		racket_indicator.position.z = right_wrist.z;
	}

	if (!anim_options.paused) {
		frame_idx += anim_options.speed * clock.getDelta() * fps;
		if (frame_idx > frame_count - 1) {
			frame_idx = 0;
		}
	}
	renderer.render(scene, camera);
};

// setup GUI
var gui = new dat.GUI();

var shot_gui = gui.addFolder("shot");
shot_gui.add(shot_options, 'next_shot');
shot_gui.add(shot_options, 'prev_shot');
shot_gui.open()

var anim = gui.addFolder("animation");
anim.add(anim_options, 'speed', 0, 1).listen();
anim.add(anim_options, 'pause');
anim.add(anim_options, 'play');
anim.add(anim_options, 'step_size', 0, 10).listen();
anim.add(anim_options, 'step_forward');
anim.add(anim_options, 'step_backward');

animate();
