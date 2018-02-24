function zeros(dims) {
    var array = [];
    for (var i = 0; i < dims[0]; ++i) {
        array.push(dims.length == 1 ? 0 : zeros(dims.slice(1)));
    }
    return array;
}

var sqr_len = 10;
var sqr_height = 50;
var sqr_width = 80;
var cnv_len = [sqr_width * (sqr_len + 1) - 1, sqr_height * (sqr_len + 1) - 1];
var life = zeros([sqr_width, sqr_height]);
var neib_table = zeros([sqr_width, sqr_height]);

function validate_point(point){
	return point[0] >= 0 && point[0] < sqr_width - 1 && point[1] >= 0 && point[1] < sqr_height - 1;
}

function live_check(point){
	return life[point[0]][point[1]] == 1 ? true : false;
}

function neighbours(point){
	var num_neibs = 0;
	var neibs = [[point[0] - 1, point[1] - 1],
				 [point[0] - 1, point[1] + 1],
				 [point[0] - 1, point[1]],
				 [point[0] + 1, point[1] - 1],
				 [point[0] + 1, point[1] + 1],
				 [point[0] + 1, point[1]],
				 [point[0], point[1] - 1],
				 [point[0], point[1] + 1]]
    for(var i = 0; i < 8; ++i){
    	if(validate_point(neibs[i]) && live_check(neibs[i]))
    		num_neibs += 1;
    }
    return num_neibs;
}


function setup(){
	var canvas = createCanvas(cnv_len[0], cnv_len[1]);
	canvas.parent('game');
	canvas.style('margin', 'auto');
	canvas.style('display', 'block');
	frameRate(20);
}

var start = false

function draw(){

	if(mouseIsPressed && !start){
		var x = mouseX;
		var y = mouseY;
		if( x % (sqr_len + 1) != 0 && y % (sqr_len + 1) != 0 ){
			sqr_x = floor(x / (sqr_len + 1));
			sqr_y = floor(y / (sqr_len + 1));
			life[sqr_x][sqr_y] = 1;
		}
	}

	else if(keyIsPressed && keyCode == ENTER) start = true;
	else if(keyIsPressed && keyCode == BACKSPACE){
		start = false;
		for(var x = 0; x < sqr_width; x += 1){
			for(var y = 0; y < sqr_height; y += 1){
				life[x][y] = 0;
			}
		}
	}

	else if(start){

		for(var x = 0; x < sqr_width; x += 1){
			for(var y = 0; y < sqr_height; y += 1){
				neib_table[x][y] = neighbours([x, y]);
			}
		}

		for(var x = 0; x < sqr_width; x += 1){
			for(var y = 0; y < sqr_height; y += 1){
				num_neibs = neib_table[x][y];
				if(num_neibs < 2) life[x][y] = 0;
				else if(num_neibs == 3) life[x][y] = 1;
				else if(num_neibs > 3) life[x][y] = 0;
			}
		}
	}

	// This block of code draws the grid and live cells - *****************
	background(128, 110, 79); stroke(157, 147, 114);

	for (var row = sqr_len; row < cnv_len[1]; row += sqr_len + 1){
		line(0, row, cnv_len[0], row);
	}
	for (var col = sqr_len; col < cnv_len[0]; col += sqr_len + 1){
		line(col, 0, col, cnv_len[1]);
	}

	noStroke(); fill(91, 70, 45);

	for(var x = 0; x < sqr_width; x += 1)
		for(var y = 0; y < sqr_height; y += 1)
			if(life[x][y] == 1)
				rect(x * (sqr_len+1), y * (sqr_len+1), sqr_len, sqr_len);		

	//*********************************************************************

}