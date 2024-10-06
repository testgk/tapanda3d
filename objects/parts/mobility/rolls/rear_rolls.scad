
// Tank dimensions
tank_length = 100;
tank_width = 60;
tank_height = 30;





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

    translate( [ -track_length/3,0, 0 ] )
    wheel(track_width,track_height * 1.8);
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


tracks();
