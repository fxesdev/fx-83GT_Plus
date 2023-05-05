scale = 3;

window.onload = function() {
	// Create a canvas
	var canvas = document.createElement('canvas');
	var ctx = canvas.getContext('2d');

	// Load the font onto the canvas
	var img = new Image;
	img.onload = function() {
		// Set the correct size and disable anti-aliasing
		canvas.width = img.width * scale;
		canvas.height = img.height * scale;
		ctx.imageSmoothingEnabled = false;

		// Draw the image and store the context
		ctx.drawImage(img, 0, 0, img.width * scale, img.height * scale);
		window.calcFontCtx = ctx;
	};
	img.src = "font.png";

	// Disable image smoothing on drawing canvas and set size
	var drawing_canvas = document.getElementById('text_render');
	drawing_canvas.width = window.screen.width;
	drawing_canvas.getContext('2d').imageSmoothingEnabled = false

	// Add listener on the text box
	document.getElementById('text_input').addEventListener('input', updateRender)

	// Load character-to-byte mappings
	var xhr = new XMLHttpRequest();
	xhr.open('GET', 'characters.json', true);
	xhr.responseType = 'json';
	xhr.onload = function() {
	  map = xhr.response;
	  Object.keys(map).forEach(function(key) {
		map[key] = Array.from(atob(map[key]), c => c.charCodeAt(0));
	  });
	  window.characterMap = map;
	};
	xhr.send();
}

function getChar(c) {
	// Get x and y coordinates
	x = c % 16;
	y = Math.floor(c/16);

	x *= 8 * scale;
	y *= 9 * scale;

	return window.calcFontCtx.getImageData(x, y, 8 * scale, 9 * scale);
}

function renderBytes(bytes) {
	// Get canvas context
	var canvas = document.getElementById('text_render');
	var ctx = canvas.getContext('2d');

	// Clear the canvas
	ctx.clearRect(0, 0, canvas.width, canvas.height);
	
	// Loop over and render every character
	for(var i = 0; i < bytes.length; i++) {
		ctx.putImageData(getChar(bytes[i]), 8*scale*i, 0);
	}
}

function renderString(string) {
	bytes = new Array();
	for(var i = 0; i < string.length; i++) {
		bytes = bytes.concat(window.characterMap[string[i]]);
	}
	renderBytes(bytes);
}

function updateRender(e) {
	// Convert from hex to bytes
	string = e.target.value.split(" ").map(i => parseInt(i, 16));
	if (string.includes(NaN)) return;
	renderString(string);
}