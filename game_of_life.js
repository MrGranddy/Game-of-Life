let box_w = 60;
let box_h = 40;
let box_e = 15;

let width = box_w * box_e + 1
let height = box_h * box_e + 1

let life_table = [];
for(let col = 0; col < box_w; ++col){
	life_table[col] = [];
	for(let row = 0; row < box_h; ++row){
		life_table[col][row] = false;
	}
}

let neighbour_table = [];
for(let col = 0; col < box_w; ++col){
	neighbour_table[col] = [];
	for(let row = 0; row < box_h; ++row){
		neighbour_table[col][row] = 0;
	}
}



function setup(){

	createCanvas(width, height);
}

function draw(){
	if(mouseIsPressed){
		fill(0);
	}
	else{
		fill(255);
	}
	ellipse(mouseX, mouseY, 80, 80);
}