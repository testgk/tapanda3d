
TOWER_HEIGHT = 30;
TOWER_BOTTOM = 10;



module tower( tower_height, tower_bottom, wall, ratio ){
    difference(){
        cylinder( h = tower_height, r1 = tower_bottom, r2 = tower_bottom * ratio, center = true);
        cylinder( h = tower_height + 1, r1 = tower_bottom - wall , r2 = tower_bottom * 0.8 - wall, center = true );
    }
}

module gear(teeth = 10, radius = 15, thickness = 8, tooth_height = 20) {
    angle = 360 / teeth;
    difference() {
        cylinder(h = thickness, r = radius, $fn = 100);
        for (i = [0: teeth - 1  ] ) {
            rotate( [ 0, 0, i * angle  ] ) {
                translate( [ radius, 0, 0  ] ) {
                    rotate( [ 0, 90, 0  ] ) {
                        translate( [ -tooth_height/2, -radius/teeth, -thickness/2  ] )
                            cube( [ tooth_height, 2*radius/teeth, thickness  ] );
                    }
                }
            }
        }
    }
}

module platform( radius = TOWER_BOTTOM*0.8, rTop = 0.6 * TOWER_BOTTOM )
{
    d = radius - sqrt( pow(radius,2) - pow(rTop,2));
    translate( [0,0, TOWER_HEIGHT/2 + radius - d])
    difference(){
       sphere( r = radius);
       translate( [0,0,radius])
       cube( radius * 2, center = true );
    }
}
module small_tower() {
    difference() {
        tower(tower_height = TOWER_HEIGHT, tower_bottom = TOWER_BOTTOM, wall = TOWER_HEIGHT/10, ratio = 0.6 );
        translate( [ 0, 0, -15 ] )
            gear(radius = 10, thickness = 5, tooth_height = 12 );
        translate( [ 0, 0, -8 ] )
            gear(radius = 10, thickness = 6, tooth_height = 15 );
        gear(radius = 10, thickness = 6, tooth_height = 13 );
        translate([ 0, 0, 8 ])
            gear(radius = 8, thickness = 4, tooth_height = 8 );
    }
}



small_tower();
platform();

