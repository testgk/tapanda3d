// Simple Tank Model in OpenSCAD
use <track.scad>

// Tank dimensions
tank_length = 100;
tank_width = 60;
tank_height = 30;
turret_diameter = 40;
turret_height = 20;
barrel_length = 50;
barrel_diameter = 5;

// Tank body
module tank_body() {
    hull();
}

// Hull
module hull() {
    translate([ 0, 0, tank_height / 2 ] )
        cube( [ tank_length, tank_width, tank_height ], true );
}

difference(){
tank_body();
trackspace();
}
tracks();
