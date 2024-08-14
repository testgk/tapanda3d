


difference(){
cube([ 20, 20 , 5], center = true);
    translate([ 0,0,2 ])
        cylinder( h = 3, r = 8, center = true);
}


translate([ 0,0,10/2 + 2])
    difference(){
        cylinder( h = 10, r1 = 7.5, r2 = 4, center = true);
        translate([ 0, 0, 10])
            cylinder( h = 16, r = 3.8, center= true);
    }

   translate([ 0,0,10])
        cylinder( h = 8, r = 3.3,center = true);
        translate([ 0,0,18])
        sphere(4);