import math

from panda3d.core import GeomVertexReader, GeomNode, NodePath, GeomVertexFormat, GeomVertexData, GeomVertexWriter, Geom, \
	GeomTriangles, CollisionPolygon, GeomLines, Vec3, LVecBase3f

from enums.colors import Color
from selectionitem import SelectionItem
from selectionmodes import SelectionModes
from target import Target


def getNodePosition( name ):
	pos = name[ 3: ].split( 'x' )
	return int( pos[ 0 ] ), int( pos[ 1 ] )


def getVertices( geom: GeomNode ) -> list:
	all_vertices = [ ]
	tris = geom.getPrimitive( 0 )  # Assuming the first primitive is triangles
	tris = tris.decompose()
	vertex_data = geom.getVertexData()
	vertex_reader = GeomVertexReader( vertex_data, 'vertex' )
	primitives = tris.getNumPrimitives()
	for i in range( tris.getNumPrimitives() ):
		prim_start = tris.getPrimitiveStart( i )
		prim_end = tris.getPrimitiveEnd( i )
		assert prim_end - prim_start == 3

		vertices = [ ]
		for pr_index in range( prim_start, prim_end ):
			vi = tris.getVertex( pr_index )
			vertex_reader.setRow( vi )
			v = vertex_reader.getData3()
			vertices.append( v )
		all_vertices.append( vertices )
	return all_vertices


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


def createWireNode( customNode ):
	vertex_format = GeomVertexFormat.getV3()
	wire_vertex_data = GeomVertexData( 'wire_vertices', vertex_format, Geom.UHDynamic )
	wire_vertex_writer = GeomVertexWriter( wire_vertex_data, 'vertex' )
	lines = GeomLines( Geom.UHDynamic )

	wire_vertex_count = 0
	for i in range( customNode.getNumSolids() ):
		poly = customNode.getSolid( i )
		if isinstance( poly, CollisionPolygon ):
			num_points = poly.getNumPoints()
			poly_vertices = [ ]
			for j in range( num_points ):
				point = poly.getPoint( j )
				poly_vertices.append( point )
			# Create lines for the wireframe
			for j in range( num_points ):
				start_point = poly_vertices[ j ]
				end_point = poly_vertices[ (j + 1) % num_points ]
				wire_vertex_writer.addData3f( start_point )
				wire_vertex_writer.addData3f( end_point )
				lines.addVertices( wire_vertex_count, wire_vertex_count + 1 )
				wire_vertex_count += 2

	wire_geom = Geom( wire_vertex_data )
	wire_geom.addPrimitive( lines )
	wire_geom_node = GeomNode( 'wire_geom' )
	wire_geom_node.addGeom( wire_geom )
	return wire_geom_node



class CustomPolygon( SelectionItem, Target ):
	def __init__( self, child: NodePath ):
		self._child = child
		self._name = self._child.getName()
		self._vertices = getVertices( self._child.node().getGeom( 0 ) )
		self._debug_node_path = None
		self._wire_node_path = None
		for vertex in self._vertices:
			self._angle = calculate_angle( vertex )
			self._area = triangle_area( vertex[ 0 ], vertex[ 1 ], vertex[ 2 ] )
			self._row, self._col = getNodePosition( self._name )
		self._isTerrain = True
		self._selectionMode = SelectionModes.NONE

	@property
	def position( self ):
		return self._child.get_pos()

	def hpr( self, model ):
		return self._child.getHpr( model )

	def getPos( self, model ):
		return self._child.get_pos( model )

	@property
	def isTerrain( self ):
		return True

	@property
	def isTerrain( self ):
		return True

	@property
	def isObstacle( self ):
		return False

	@property
	def row( self ):
		return self._row

	@property
	def col( self ):
		return self._col

	def __str__( self ):
		return ( f'{ self._name }, row: { self._row }, column: { self._col }, '
		        f'area: { self._area }, angle: { self._angle }')

	def _generateDebugNodePath( self, height_offset ):
		debug_geom_node = self.createDebugNode()
		self._debug_node_path = self._child.attachNewNode( debug_geom_node )
		self._debug_node_path.setZ( self._debug_node_path.getZ() + height_offset )
		self._debug_node_path.hide()
		return self._debug_node_path

	def _generateWireNodePath( self, customNode, height_offset ):
		wire_geom_node = createWireNode( customNode )
		self._wire_node_path = self._child.attachNewNode( wire_geom_node )
		self._wire_node_path.setZ( self._debug_node_path.getZ() + height_offset )
		self._wire_node_path.setColor( Color.CYAN)
		self._wire_node_path.setRenderModeWireframe()
		self._wire_node_path.hide()

	def _attachDebugNode( self, customNode, height_offset = 0.1 ):
		g = self._generateDebugNodePath( height_offset )
		self._generateWireNodePath( customNode, height_offset )

	def _showDebugNode( self ):
		self._visible = True
		self._debug_node_path.show()

	def _colorDebugNode( self, color = Color.RED_TRANSPARENT):
		self._debug_node_path.setColor( color )  # Set the color to red
		self._debug_node_path.setTransparency( True )

	def createDebugNode( self ):
		return self.createDebugNodeGeomNode( self._vertices )

	def handleSelection( self, mode: SelectionModes = SelectionModes.ANY ):
		print( f'{ self._name } selection mode: { mode }' )

	def clearSelection( self ):
		print( f'{ self._name } selection cleared' )

	def createDebugNodeGeomNode( self, vertices ):
		debug_geom_node = GeomNode( 'debug_geom' )
		vertex_format = GeomVertexFormat.getV3()  # Position only
		vertex_data = GeomVertexData( 'vertices', vertex_format, Geom.UHDynamic )
		vertex_writer = GeomVertexWriter( vertex_data, 'vertex' )
		geom = Geom( vertex_data )

		vertex_count = 0
		tris = GeomTriangles( Geom.UHDynamic )

		# Iterate through the list of lists of LVecBase3f
		for triangle in vertices:
			for vertex in triangle:
				# Each `vertex` is an LVecBase3f, so we access its components
				vertex_writer.addData3f( vertex.x, vertex.y, vertex.z )
				tris.addVertex( vertex_count )
				vertex_count += 1

			# Close the triangle primitive after 3 vertices
			tris.closePrimitive()

		geom.addPrimitive( tris )
		debug_geom_node.addGeom( geom )
		return debug_geom_node
