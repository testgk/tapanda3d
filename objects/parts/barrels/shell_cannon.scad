
//Overall Tank Dimensions
tank_length = 100;
tank_width = 60;

//Parts Dimensions
hull_width = 0;
hull_height = 0;
tank_height = 30;
track_width = 30;
track_height = 20;
turret_height = 20;
cannon_length =40;


track_length = tank_length * 0.9;
turret_radius = tank_width / 3;



module track( ){
     cube( [ track_length, track_width, track_height ], true );
     translate( [ track_length / 2,track_width / 2, 0 ] )
        wheel( track_width,track_height );
     translate( [ -track_length / 2, track_width/2, 0 ] )
        wheel(track_width,track_height);
}

module innertrack(){
     cube( [ track_length , track_width + 1, track_height * 0.8 ], true );
     translate( [ track_length / 2, track_width/2 + 2, 0 ] )
        wheel( track_width + 4,track_height * 0.8 );
     translate( [ -track_length / 2 , track_width/2 + 2, 0 ] )
        wheel(track_width + 4,track_height * 0.8 );
}

module wheel( width, diameter ){
    color( "purple")
         rotate( [ 90, 0, 0 ] ){
         cylinder( h = width, r = diameter / 2 );
    } 
}

module fulltrack( ){

    difference(){
    track();
    color( "green") innertrack();
    }
    
    translate([ 0,track_width/2,0] ){
        wheel(track_width/2,track_height);
        translate( [ track_length/3 ,0, 0 ] )
        wheel(track_width/2,track_height);
        translate( [-track_length/3,0, 0 ] )
        wheel(track_width/2,track_height);
    }
} 

module tracks(){
    translate( [ 0, -tank_width / 2, 0 ] )
        mirror([0,1,0])
        fulltrack();
    
    translate( [ 0, tank_width / 2, 0 ] )
        fulltrack();  
}

module hull(){
    color( "blue")
    difference(){
    translate( [ 0, 0, tank_height / 4 ] )
    cube( [ tank_length,tank_width ,3 * tank_height / 4 ], center = true);
      translate( [ 0, tank_width / 2, 0 ] )
        track();
      translate( [ 0, -tank_width / 2, 0 ] )
        track();
    }
}

module turret(){
    translate( [ 0, 0, tank_height  ] )
      cylinder( h = turret_height, r = tank_width/3, center = true  );
}

module cannon()
{
    translate( [ cannon_length/2 + turret_radius, 0, tank_height  ] )
    rotate( [0, 90, 0])
    {
            difference() {
                cylinder(h = cannon_length, r = 5, center = true);
                cylinder(h = cannon_length + 2, r = 2, center = true);
            }
                
            
    }
    
}


//tracks();
//hull();
//turret();
cannon();
