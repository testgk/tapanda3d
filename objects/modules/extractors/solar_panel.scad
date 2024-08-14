

module edges(){
color("red")
difference(){
cube([ 21,21,7], center = true);
    rotate( [0,0,45])
        cube([ 21,21,7], center = true);
}
}

difference(){
    cube([ 20,20,5], center = true);
    edges();
}
