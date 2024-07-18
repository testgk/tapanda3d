from panda3d.core import GeomVertexFormat, GeomVertexData, Geom, GeomVertexWriter, GeomTriangles, GeomNode


def create_cube() :
    # Define the format of the vertex data
    format = GeomVertexFormat.get_v3n3()

    # Create the vertex data structure
    vertex_data = GeomVertexData( "vertices", format, Geom.UH_static )

    # Add vertices
    vertex_writer = GeomVertexWriter( vertex_data, "vertex" )
    normal_writer = GeomVertexWriter( vertex_data, "normal" )

    # Define vertices and normals for a cube
    vertices = [
        (-1, -1, -1),
        (1, -1, -1),
        (1, 1, -1),
        (-1, 1, -1),
        (-1, -1, 1),
        (1, -1, 1),
        (1, 1, 1),
        (-1, 1, 1)
    ]

    normals = [
        (0, 0, -1),
        (0, 0, 1),
        (0, -1, 0),
        (0, 1, 0),
        (-1, 0, 0),
        (1, 0, 0)
    ]

    # Write vertices and normals
    for v in vertices :
        vertex_writer.add_data3( v[ 0 ], v[ 1 ], v[ 2 ] )

    for n in normals :
        normal_writer.add_data3( n[ 0 ], n[ 1 ], n[ 2 ] )

    # Create the primitive (triangles)
    primitive = GeomTriangles( Geom.UH_static )

    # Define triangles
    triangles = [
        (0, 1, 2), (2, 3, 0),  # Bottom
        (4, 5, 6), (6, 7, 4),  # Top
        (0, 1, 5), (5, 4, 0),  # Front
        (2, 3, 7), (7, 6, 2),  # Back
        (0, 3, 7), (7, 4, 0),  # Left
        (1, 2, 6), (6, 5, 1)  # Right
    ]

    # Add triangles to the primitive
    for tri in triangles :
        primitive.add_vertices( tri[ 0 ], tri[ 1 ], tri[ 2 ] )

    # Create a geometry object
    geom = Geom( vertex_data )
    geom.add_primitive( primitive )

    # Create a geometry node
    geom_node = GeomNode( "cube" )
    geom_node.add_geom( geom )

    return geom_node