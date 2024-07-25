
// Tank dimensions
tank_length = 100;
tank_width = 60;
tank_height = 30;




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
    track_width = w;
    track_height = h;
    track_length = l;

    //translate( [ 0, w / 2, 0 ] )
    difference(){
    track( track_length,track_width,tank_height );
    track( track_length,track_width + 1,tank_height * 0.8 );
    }
    
    wheel(track_width,track_height * 1.15);
    translate( [track_length/3,0, 0 ] )
    wheel(track_width,track_height * 1.15);
    translate( [-track_length/3,0, 0 ] )
    wheel(track_width,track_height * 1.15);
} 

module tracks(){
    track_width = 10;
    track_height = tank_height / 1.5;
    track_length = tank_length * 0.9;

    translate( [ 0, -tank_width / 2, 0 ] )
        fulltrack( 20, tank_height / 1.5, tank_length * 0.9);
    
    
    translate( [ 0, tank_width / 2, 0 ] )
        fulltrack( 20, tank_height / 1.5, tank_length * 0.9);
    
}

module trackspace()
{   
    track_width = 20;
    track_height = tank_height / 1.2;
    track_length = tank_length + 1;
    translate( [ 0, -tank_width /  2, 0 ] )
        cube( [ track_length, track_width, track_height ], true );
    
    
    translate( [ 0, tank_width / 2 , 0 ] )
        cube( [ track_length, track_width, track_height ], true );    
}

//trackspace();
tracks();
//track_right();
