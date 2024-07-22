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
    translate([0, 0, tank_height / 2])
        cube([tank_length, tank_width, tank_height], true);
}

// Tracks
module tracks() {
    track_width = 10;
    track_height = tank_height/2;
    track_length = tank_length * 0.9;

    translate([0, -tank_width / 2, 0])
        cube([track_length, track_width, track_height], true);

    translate([0, tank_width / 2, 0])
        cube([track_length, track_width, track_height], true);
}

// Turret
module turret() {
    translate([0, 0, tank_height + turret_height / 2])
        cylinder(h = turret_height, r = turret_diameter / 2, center = true);
}

// Barrel
module barrel() {
    translate([0, 0, tank_height + turret_height])
        rotate([0, 90, 0])
        translate([(turret_height / 2 ), 0, (barrel_length/2)])
        cylinder(h = barrel_length, r = barrel_diameter / 2, center = true);
}

// Assemble the tank
module tank() {
    tank_body();
    turret();
    barrel();
}

tank();
