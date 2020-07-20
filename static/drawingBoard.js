// drawingBoard.js

let dim;

function setup() {
	canvas = createCanvas(displayWidth, displayHeight);
	canvas.position(0, 0, 'fixed');
	dim = width / 2;
	background(0);
	colorMode(HSB, 360, 100, 100);
	noStroke();
	ellipseMode(RADIUS);
	noLoop();
	// frameRate(1);
}

function draw() {
	background(0);
	drawGradient(width/2, height/2.5);
}

function drawGradient(x, y) {
	let radius = width*1.5;
	let c = [100, 0, 0, 0.0];
	let b = [, 0, 0, 1.0];
	for (let r = radius; r > 0; --r) {
		let curr = [];
		for (let i=0; i<c.length; i++) {
			curr.push((r*(b[i]-c[i]))/radius+c[i]);
		}
		let currFill = `rgba(${curr[0]}%, ${curr[1]}%, ${curr[2]}%, ${curr[3]})`;
		fill(currFill);
		ellipse(x, y, r, r*1.5);
	}
}