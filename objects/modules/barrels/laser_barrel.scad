
module triangle_prism(base_length, prism_height) {
    triangle_height = sqrt(3) / 2 * base_length;
    x_offset = base_length / 2;
    z_offset = prism_height / 2;
    y_offset = triangle_height / 2;
    vertices = [
        [-x_offset, -y_offset, -z_offset],  // Vertex 0
        [x_offset, -y_offset, -z_offset],   // Vertex 1
        [0, y_offset, -z_offset],           // Vertex 2
        [-x_offset, -y_offset, z_offset],   // Vertex 3 (top)
        [x_offset, -y_offset, z_offset],    // Vertex 4 (top)
        [0, y_offset, z_offset]             // Vertex 5 (top)
    ];

    faces = [
        [0, 1, 2],  // Base triangle
        [3, 4, 5],  // Top triangle
        [0, 1, 4, 3], // Side face 1
        [1, 2, 5, 4], // Side face 2
        [2, 0, 3, 5]  // Side face 3
    ];

    polyhedron(points = vertices, faces = faces);
}





// Parameters
base_length = 10; // Length of the base of the triangle
prism_height = 100; // Height of the triangular prism


rotate( [0,90,0] )
    triangle_prism(base_length,prism_height);
