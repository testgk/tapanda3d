
// Tank dimensions
tank_length = 100;
tank_width = 60;
tank_height = 30;
track_width = 10;
track_height = 20;
track_length = tank_length * 0.9;




module track( track_length, track_width, track_height ){
     cube( [ track_length, track_width, track_height ], true );
     translate( [ track_length / 2, 0, 0 ] )
        wheel( track_width,track_height );
     translate( [ -track_length / 2, 0, 0 ] )
        wheel(track_width,track_height);
}

module wheel( track_width,track_height ){
         translate( [0, track_width/2, 0 ] )
         rotate( [ 90, 0, 0 ] ){
         cylinder( h = track_width, r = track_height / 2 );
    } 
}

module fulltrack( w, h, l ){

    difference(){
    track( l,w,tank_height );
    track( l,w + 1,tank_height * 0.8 );
    }
    
    wheel(w,h * 1.15);
    translate( [l/3,0, 0 ] )
    wheel(w,h * 1.15);
    translate( [-track_length/3,0, 0 ] )
    wheel(w,h * 1.15);
} 

module tracks(){


    translate( [ 0, -tank_width / 2, 0 ] )
        fulltrack( track_height, track_height, track_length);
    
    
    translate( [ 0, tank_width / 2, 0 ] )
        fulltrack( track_height, track_height, track_length);
    
}

module hull(){
    translate([0,0,tank_height/4]){
    cube([ tank_length,tank_width - track_width*2,tank_height/2], center = true);
    }
    translate([0,0,tank_height/1.5])
        cube([ tank_length,tank_width,tank_height/3], center = true);
}




tracks();
//hull();

//track_right();
