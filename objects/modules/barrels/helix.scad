



module helix( twists, twist_height ){
    translate( [ -( twists + 1 )* twist_height/2, 0, 0 ] ){
    rotate( [ 0, 90, 0 ] ){
        for(i = [ 1 : twists ] )
        translate( [ 0, 0, i * twists ] )
            linear_extrude( height = twist_height, center = false, convexity = 10, twist = 360, $fn = 100 )
            translate( [ twist_height, 0, 0 ] )
            circle( r = 3 );
        }
    }
}



// Parameters
base_length = 10; // Length of the base of the triangle
height = sqrt(3) / 2 * base_length; // Height of the equilateral triangle
prism_height = 100; // Height of the triangular prism


helix( twists = 10, twist_height = 10 );




