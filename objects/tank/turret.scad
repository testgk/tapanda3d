// Simple Tank Model in OpenSCAD

// Tank dimensions
tank_length = 100;
tank_width = 60;
tank_height = 30;
turret_diameter = 40;
turret_height = 20;
barrel_length = 50;
barrel_diameter = 5;


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
    turret();
    barrel();
}

tank();
