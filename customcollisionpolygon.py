import math
from typing import Any

from panda3d.core import BitMask32, CollisionNode, CollisionPolygon, DirectionalLight, GeomVertexReader, LVector4, \
    NodePath, Vec3, \
    GeomVertexFormat, GeomVertexData, GeomVertexWriter, GeomTriangles, Geom, GeomNode, Vec4, Point3, GeomLines, \
    GeomPoints


def getPolygonFromPool( row, column ) -> Any | None:
    try:
        return polygons[ f"gmm{ row }x{ column }" ]
    except KeyError:
        return None


def getPolygonByName( name: str ) -> 'CustomCollisionPolygon':
    return polygons[ name ]

def addPolygonToPool( name, polygon ):
    polygons[ name ] = polygon


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


def getPointGeomNode( point ) :
     print( f' drawing point {point}' )
     vertex_format = GeomVertexFormat.get_v3()
     vertex_data = GeomVertexData( "vertices", vertex_format, Geom.UHStatic )
     vertex_writer = GeomVertexWriter( vertex_data, "vertex" )
     vertex_writer.add_data3( point )
     points = GeomPoints( Geom.UHStatic )
     points.add_next_vertices( 1 )
     geom = Geom( vertex_data )
     geom.add_primitive( points )
     geom_node = GeomNode( "point_node" )
     geom_node.add_geom( geom )
     return geom_node


polygons = { }
currentFrame = []



def calculate_angle( vertex, reference_plane_normal = Vec3( 0, 0, 1 ) ):
    edge1 = vertex[ 1 ] - vertex[ 0 ]
    edge2 = vertex[ 2 ] - vertex[ 0 ]
    normal_vector = edge1.cross( edge2 ).normalized()
    dot_product = normal_vector.dot( reference_plane_normal )
    magnitude_product = normal_vector.length() * reference_plane_normal.length()
    angle_radians = math.acos( dot_product / magnitude_product )
    angle_degrees = math.degrees( angle_radians )
    return angle_degrees

def triangle_area( v0, v1, v2 ):
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
        self.__edges = {}
        self.__visible = None
        self.__neighborsDic = None
        self.__col = None
        self.__row = None
        self.__area = None
        self.__name = None
        self.__angle = None
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
            poly = CollisionPolygon( vertex[ 0 ], vertex[ 1 ], vertex[ 2 ] )
            self.__angle = calculate_angle( vertex )
            self.__name = self.__child.getName()
            self.__area = triangle_area( vertex[ 0 ], vertex[ 1 ], vertex[ 2 ] )
            self.__row, self.__col = getNodePosition( self.__name )
            print( f"{self.__name}: triangle: {triangleCount} {self.__angle}, row = {self.__row}, column = {self.__col} area = {self.__area}" )
            self.__collision_node.addSolid( poly )
            triangleCount += 1
        self.__collision_node.setPythonTag( 'custom_collision_polygon', self )
        self.__edges[ 'upright' ] = vertices[ 0 ][ 0 ]
        self.__edges[ 'upleft' ] = vertices[ 0 ][ 1 ]
        self.__edges[ 'downright' ] = vertices[ 1 ][ 1 ]
        self.__edges[ 'downleft' ] = vertices[ 1 ][ 0 ]
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

    def showNeighbors( self, startRow, startCol, level ) :
        row_diff = abs( self.row - startRow )
        col_diff = abs( self.col - startCol )

        # Check visibility and distance constraints
        if self.__visible or abs( row_diff) > level or abs( col_diff ) > level :
            return

        self.__displayEdges( level, col_diff, row_diff, startCol, startRow )
        self.showDebugNode()
        self.colorDebugNode()
        self.__visible = True
        for neighbor in self.__neighborsDic.values() :
            neighbor.showNeighbors( startRow, startCol, level )

    def __displayEdges( self, level, col_diff, row_diff, startCol, startRow ) :
        if row_diff == level and col_diff == level :
            self.__showFrame()
            # Handle diagonal cases
            if self.row > startRow and self.col < startCol :  # Down
                self.__drawEdges( 'upleft', 'upright' )
            elif self.row < startRow and self.col > startCol :  # Up left
                self.__drawEdges( 'downright', 'downleft' )
            elif self.row > startRow and self.col > startCol :  # Up right
                self.__drawEdges( 'upleft', 'downleft' )
            else :  # Down left
                self.__drawEdges( 'upright', 'downright' )

        elif row_diff == level and col_diff < level :
            # Handle vertical edge cases
            if self.row > startRow :
                self.__drawEdges( 'upleft' )
            elif self.row < startRow :
                self.__drawEdges( 'downright' )

        elif row_diff < level and col_diff == level :
            # Handle horizontal edge cases
            if self.col > startCol :
                self.__drawEdges( 'downleft' )
            elif self.col < startCol :
                self.__drawEdges( 'upright' )

    def __showFrame( self, color = Vec4( 0, 1, 0, 0.5 ) ):
        self.__wire_node_path.setColor( color )
        self.__wire_node_path.show()

    def hideNeighbors( self ):
        if self.__visible:
            self.__hideDebugNode()
            for neighbor in self.__neighborsDic.values():
                neighbor.hideNeighbors()

    def __hideDebugNode( self ):
        self.__visible = False
        self.__debug_node_path.hide()
        self.__wire_node_path.hide()

    def showDebugNode( self ):
        self.__visible = True
        self.__debug_node_path.show()

    def __drawEdges( self, *args ):
        for direction in args:
            point = Point3( self.__edges[ direction ] )
            print( f'point: {point}' )
            self.__draw_point( point )

    def removeAllEdges( self ):
        for edge in currentFrame:
            edge.remove_node()
        currentFrame.clear()

    def __draw_point( self, point: Point3 ):
        geom_node = getPointGeomNode( point )
        __point_node_path = self.__child.attachNewNode( geom_node )
        __point_node_path.setZ( __point_node_path.getZ() + 0.02 )
        __point_node_path.set_render_mode_thickness( 5 )
        __point_node_path.setColor( Vec4( 0, 1, 0, 0.5 ) )
        currentFrame.append( __point_node_path )

    def __str__( self ):
        return (f'{ self.__name }, row: { self.__row }, column: { self.__col }, '
                f'area: { self.__area }, angle: { self.__angle }')

    def attachToTerrainChildNode( self, height_offset = 0.1 ):
        self.__collision_node_path = self.__child.attachNewNode( self.__collision_node )
        self.__collision_node_path.setRenderModeWireframe()
        self.__collision_node_path.setRenderModeThickness( 2 )
        self.__collision_node_path.setColor( Vec4( 1, 1, 0, 0.5 ) )
        self.__collision_node_path.setZ( self.__collision_node_path.getZ() + height_offset )
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

        self.__debug_node_path = self.__child.attachNewNode( debug_geom_node )
        self.__debug_node_path.setZ( self.__debug_node_path.getZ() + height_offset )
        self.__debug_node_path.hide()

        self.__wire_node_path.setZ( self.__debug_node_path.getZ() + height_offset )
        self.__wire_node_path.setColor( Vec4( 0, 1, 0, 0.5 ) )
        self.__wire_node_path.hide()
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
