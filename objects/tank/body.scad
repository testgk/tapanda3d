// Simple Tank Model in OpenSCAD

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
    tracks();
}

// Hull
module hull() {
    translate([ 0, 0, tank_height / 2 ] )
        cube( [ tank_length, tank_width, tank_height ], true);
}

module track(track_length,track_width,track_height){
     cube( [ track_length, track_width, track_height ], true);
     translate([ track_length/2, track_width / 2, 0 ] )
        wheel(track_width,track_height);
     translate([ -track_length/2, track_width / 2, 0 ] )
        wheel(track_width,track_height);
}

module wheel( track_width,track_height){
         rotate([90, 0, 0]){
         cylinder( h = track_width, r = track_height/2 );
    } 
}

// Tracks
module tracks() {
    track_width = 10;
    track_height = tank_height / 2;
    track_length = tank_length * 0.9;

    translate( [ 0, -tank_width / 2, 0 ] )
        track( track_length,track_width,track_height);

   // translate( [ 0, tank_width / 2, 0] )
   //     track(track_length,track_width,track_height);
}

// Assemble the tank
module tank() {
    tracks();
}

tank();
