// drawingBoard.js

let dim;

function sigmoid(x) {
	let a = Math.exp(x);
	return a/(1+a);
}

function bell_pieceWise(x) {
	let b = 0.7;
	let top = 1;
	let bottom = 100;
	if (x>=b) {
		return (x-b)*top;
	}
	else {
		return (x-b)*bottom;
	}
}

function grad(x, shift, scale, func) {
	let top = func(1.0*scale);
	let bottom = func(-1.0*scale);
	return (func(x)-bottom)/(top-bottom);
}

function setup() {
	canvas = createCanvas(displayWidth, displayHeight);
	canvas.position(0, 0, 'fixed');
	dim = width / 2;
	background(255);
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
	let radius = height*0.7;
	let b = [0.0, 50.0, 100.0, 0.6];
	let c = [100.0, 100.0, 100.0, 1.0];
	for (let r = radius; r > 0; --r) {
		let curr = [];
		for (let i=0; i<c.length; i++) {
			let res = r/radius-0.5;
			curr.push(grad(res, 0, 1, bell_pieceWise)*(b[i]-c[i])+c[i]);
		}
		let currFill = `rgba(${curr[0]}%, ${curr[1]}%, ${curr[2]}%, ${curr[3]})`;
		fill(currFill);
		ellipse(x, y, r*2, r);
	}
}