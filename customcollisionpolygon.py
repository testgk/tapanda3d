import math
from typing import Any

from panda3d.core import BitMask32, CollisionNode, CollisionPolygon, DirectionalLight, GeomVertexReader, LVector4, \
    NodePath, Vec3, \
    GeomVertexFormat, GeomVertexData, GeomVertexWriter, GeomTriangles, Geom, GeomNode, Vec4, Point3, GeomLines, \
    GeomPoints, LVecBase3f


def getPolygonFromPool( row, column ) -> Any | None:
    try:
        return polygons[ f"gmm{ row }x{ column }" ]
    except KeyError:
        return None


def getPolygonByName( name: str ) -> 'CustomCollisionPolygon':
    return polygons[ name ]

def addPolygonToPool( name, polygon ):
    polygons[ name ] = polygon


def acquireAllNeighbors():
    for name, polygon in polygons.items():
        polygon.getNeighbors()


def getVertices(geom: GeomNode) -> list:
    all_vertices = []
    tris = geom.getPrimitive(0)  # Assuming the first primitive is triangles
    tris = tris.decompose()
    vertex_data = geom.getVertexData()
    vertex_reader = GeomVertexReader(vertex_data, 'vertex')
    primitives = tris.getNumPrimitives()
    print(f"Primitives: {primitives}")
    for i in range(tris.getNumPrimitives()):
        prim_start = tris.getPrimitiveStart(i)
        prim_end = tris.getPrimitiveEnd(i)
        assert prim_end - prim_start == 3

        vertices = []
        for pr_index in range(prim_start, prim_end):
            vi = tris.getVertex(pr_index)
            vertex_reader.setRow(vi)
            v = vertex_reader.getData3()
            vertices.append(v)
        all_vertices.append(vertices)
    return all_vertices


polygons = { }


def calculate_angle( vertex, reference_plane_normal = Vec3( 0, 0, 1 ) ):
    # Compute two edges of the polygon
    edge1 = vertex[ 1 ] - vertex[ 0 ]
    edge2 = vertex[ 2 ] - vertex[ 0 ]
    normal_vector = edge1.cross( edge2 ).normalized()
    # Calculate the angle between the normal vector and the reference plane normal
    dot_product = normal_vector.dot( reference_plane_normal )
    magnitude_product = normal_vector.length() * reference_plane_normal.length()
    angle_radians = math.acos( dot_product / magnitude_product )
    angle_degrees = math.degrees( angle_radians )
    return angle_degrees


def triangle_area( v0, v1, v2 ):
    # Use the cross product to get the area of the triangle
    edge1 = v1 - v0
    edge2 = v2 - v0
    cross_product = edge1.cross( edge2 )
    area = 0.5 * cross_product.length()
    return area

def getNodePosition( name ):
    pos = name[ 3: ].split( 'x' )
    return int( pos[ 0 ] ), int( pos[ 1 ] )

class CustomCollisionPolygon:
    def __init__( self, child: NodePath, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.__visible = None
        self.__neighborsDic = None
        self.__col = None
        self.__row = None
        self.__area = None
        self.__name = None
        self.__angle = None
        self.__poly = None
        self.__debug_node_path = None
        self.__collision_node_path = None
        self.__collision_node = None
        self.__child = child
        self.__geom = self.__child.node().getGeom( 0 )  # Assuming each GeomNode has one Geom
        self.__vertices = getVertices( self.__geom )
        self.__collision_node = CollisionNode( f'terrain_{ self.__child.getName() }' )
        self.__collision_node.setIntoCollideMask( BitMask32.bit( 1 ) )
        self.constructCollitionNode( self.__vertices ) 

    def constructCollitionNode( self, vertices ):
        triangleCount = 0
        for vertex in vertices:
            self.__poly = CollisionPolygon( vertex[ 0 ], vertex[ 1 ], vertex[ 2 ] )
            self.__angle = calculate_angle( vertex )
            self.__name = self.__child.getName()
            self.__area = triangle_area( vertex[ 0 ], vertex[ 1 ], vertex[ 2 ] )
            self.__row, self.__col = getNodePosition( self.__name )
            print( f"{self.__name}: triangle: {triangleCount} {self.__angle}, row = {self.__row}, column = {self.__col} area = {self.__area}" )
            self.__collision_node.addSolid( self.__poly )
            triangleCount += 1
            for point in vertex:
                #self.draw_point( point)
                print(f'point: { point }')
        self.__collision_node.setPythonTag( 'custom_collision_polygon', self )
        addPolygonToPool( self.__name, self )



    @property
    def vertices( self ) -> list[ GeomVertexReader ]:
        return self.__vertices

    @property
    def name( self ) -> str:
        return self.__name

    @property
    def row( self ) -> int:
        return self.__row

    @property
    def col( self ) -> int:
        return self.__col

    def getNeighbors( self ):
        neighborsDic = {
            "up": getPolygonFromPool( self.__row - 1, self.__col ),
            "down": getPolygonFromPool( self.__row + 1, self.__col ),
            "left": getPolygonFromPool( self.__row, self.__col + 1 ),
            "right": getPolygonFromPool( self.__row, self.__col - 1 ),
            "downleft": getPolygonFromPool( self.__row + 1, self.__col + 1 ),
            "downright": getPolygonFromPool( self.__row - 1, self.__col + 1 ),
            "upleft": getPolygonFromPool( self.__row + 1, self.__col - 1 ),
            "upright": getPolygonFromPool( self.__row - 1, self.__col - 1 ),
        }
        self.__neighborsDic = { pos: node for pos, node in neighborsDic.items() if node is not None }

    def getNeighborByPosition( self, key: str ) -> 'CustomCollisionPolygon':
        return self.__neighborsDic.get( key, None )

    def showNeighbors( self, origin: 'CustomCollisionPolygon', startRow, startCol, level ):
        if self.__visible:
            return

        if abs( self.row - startRow ) > level and abs( self.col - startCol ) > level:
            if self == origin.getNeighborByPosition( 'upright' ):
                origin.showFrame()
                origin.drawPoint()
            return

        if abs( self.row - startRow ) > level or abs( self.col - startCol ) > level:
            return

        self.showDebugNode()
        self.colorDebugNode()
        self.__visible = True
        for neighbor in self.__neighborsDic.values():
            neighbor.showNeighbors( self, startRow, startCol, level )

    def showFrame( self ):
        self.__wire_node_path.show()

    def hideNeighbors( self ):
        if self.__visible:
            self.hideDebugNode()
            for neighbor in self.__neighborsDic.values():
                neighbor.hideNeighbors()

    @property
    def getNeighbor( self ) -> 'CustomCollisionPolygon':
        return getPolygonFromPool( self.__row + 1, self.__col )

    @property
    def surfacePosition( self ):
        return Point3( self.__child.getPos()[ 0 ], self.__child.getPos()[ 1 ], 0 )

    def hideDebugNode( self ):
        self.__visible = False
        self.__debug_node_path.hide()
        self.__wire_node_path.hide()

    def showDebugNode( self ):
        self.__visible = True
        self.__debug_node_path.show()
        #self.__wire_node_path.show()

    def drawPoint( self ):
            self.draw_point( self.__vertices[ 1 ][2] )

    def draw_point(self, point: LVecBase3f):
        # Create a vertex format
        vertex_format = GeomVertexFormat.get_v3()

        # Create a vertex data object
        vertex_data = GeomVertexData("vertices", vertex_format, Geom.UHStatic)

        # Create a vertex writer to add vertices
        vertex_writer = GeomVertexWriter(vertex_data, "vertex")

        # Add the point to the vertex data
        vertex_writer.add_data3(point)

        # Create a GeomPoints object
        points = GeomPoints(Geom.UHStatic)
        points.add_next_vertices(1)

        # Create a Geom object
        geom = Geom(vertex_data)
        geom.add_primitive(points)

        # Create a GeomNode to hold the geometry
        geom_node = GeomNode("point_node")
        geom_node.add_geom(geom)


        __point_node_path = self.__child.attachNewNode( geom_node )
        __point_node_path.setZ( __point_node_path.getZ() + 0.02 )

        # Optionally, set the point size (e.g., make it more visible)
        __point_node_path.set_render_mode_thickness( 5 )
        __point_node_path.setColor( Vec4( 0, 1, 0, 0.5 ) )

    @property
    def getAngle( self ):
        return self.__angle

    def __str__( self ):
        return f'{ self.__name }, row: { self.__row }, column: { self.__col }, area: { self.__area }, angle: { self.__angle }'

    def attachToTerrainChildNode( self, height_offset = 0.1 ):
        # Attach the collision node to the child node
        self.__collision_node_path = self.__child.attachNewNode( self.__collision_node )
        self.__collision_node_path.setRenderModeWireframe()
        self.__collision_node_path.setRenderModeThickness( 2 )
        self.__collision_node_path.setColor( Vec4( 1, 1, 0, 0.5 ) )
        self.__collision_node_path.setZ( self.__collision_node_path.getZ() + height_offset )
        #self.__collision_node_path.hide()
        self.__collision_node_path.show()
        self.attachDebugNode()

    def attachDebugNode( self, height_offset = 0.1  ) :
        debug_geom_node = GeomNode( 'debug_geom' )

        # Geometry for filled polygons
        vertex_format = GeomVertexFormat.getV3()
        vertex_data = GeomVertexData( 'vertices', vertex_format, Geom.UHDynamic )
        vertex_writer = GeomVertexWriter( vertex_data, 'vertex' )
        geom = Geom( vertex_data )
        tris = GeomTriangles( Geom.UHDynamic )

        # Geometry for the wireframe
        wire_vertex_data = GeomVertexData( 'wire_vertices', vertex_format, Geom.UHDynamic )
        wire_vertex_writer = GeomVertexWriter( wire_vertex_data, 'vertex' )
        lines = GeomLines( Geom.UHDynamic )

        vertex_count = 0
        wire_vertex_count = 0
        for i in range( self.__collision_node.getNumSolids() ) :
            poly = self.__collision_node.getSolid( i )
            if isinstance( poly, CollisionPolygon ) :
                num_points = poly.getNumPoints()
                poly_vertices = [ ]
                for j in range( num_points ) :
                    point = poly.getPoint( j )
                    vertex_writer.addData3f( point )
                    tris.addVertex( vertex_count )
                    poly_vertices.append( point )
                    vertex_count += 1
                tris.closePrimitive()

                # Create lines for the wireframe
                for j in range( num_points - 1 ) :
                    start_point = poly_vertices[ j ]
                    end_point = poly_vertices[ ( j + 1 ) % num_points ]
                    wire_vertex_writer.addData3f( start_point )
                    wire_vertex_writer.addData3f( end_point )
                    lines.addVertices( wire_vertex_count, wire_vertex_count + 1 )
                    wire_vertex_count += 2

        geom.addPrimitive( tris )
        debug_geom_node.addGeom( geom )

        # Add wireframe geometry
        wire_geom = Geom( wire_vertex_data )
        wire_geom.addPrimitive( lines )
        self.wire_geom_node = GeomNode( 'wire_geom' )
        self.wire_geom_node.addGeom( wire_geom )
        self.__wire_node_path = self.__child.attachNewNode( self.wire_geom_node )
        self.__wire_node_path.setRenderModeWireframe()
        self.__wire_node_path.setColor( Vec4( 2, 2, 1, 1 ) )

        self.__debug_node_path = self.__child.attachNewNode( debug_geom_node )
        self.__debug_node_path.setZ( self.__debug_node_path.getZ() + height_offset )
        self.__debug_node_path.hide()

        self.__wire_node_path.setZ( self.__debug_node_path.getZ() + height_offset )
        self.__wire_node_path.setColor( Vec4( 0, 1, 0, 0.5 ) )
        self.__wire_node_path.hide()
        #__wire_node_path.hide()

        print( f"Collision node {self.__name} created and attached to terrain" )  # Debugging

    def colorDebugNode( self ):
        color = Vec4( 1, 0, 0, 0.5 )
        self.__debug_node_path.setColor( color )  # Set the color to red
        self.__debug_node_path.setTransparency( True )

    def setColorDebugNode( self, color ):
        self.__debug_node_path.setColor( color )  # Set the color to red
        self.__debug_node_path.setTransparency( True )

    @classmethod
    def acquireAllNeighbors( cls ):
        for name, polygon in polygons.items():
            polygon.getNeighbors()