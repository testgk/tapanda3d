import random
from panda3d.core import CollisionNode, CollisionPolygon, \
	NodePath, Vec3, GeomVertexFormat, GeomVertexData, GeomVertexWriter, Geom, GeomNode, Vec4, Point3, \
	GeomPoints, GeomTriangles

from enums.colors import Color
from enums.directions import Direction
from selectionitem import SelectionItem
from custompolygon import CustomPolygon
from selectionmodes import SelectionModes
from custompolygonpool import CustomPolygonPool


def getPointGeomNode( point ):
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



currentFrame = [ ]


class CustomCollisionPolygon( CustomPolygon, SelectionItem ):
	def __init__( self, child: NodePath ):
		super().__init__( child )
		SelectionItem.__init__( self )
		self.__polygonPool = CustomPolygonPool.Instance()
		self._child = child
		self._isTerrain = True
		self.__edges = { }
		self._visible = None
		self.__neighbors = None
		self.__collision_node_path = None
		self.__collision_node = CollisionNode( f'terrain_{ self._child.getName() }' )
		self.__createCollisionNode( self._vertices )
		self.__assignEdges( self._vertices )

	def __createCollisionNode( self, vertices ):
		triangleCount = 0
		for vertex in vertices:
			poly = CollisionPolygon( vertex[ 0 ], vertex[ 1 ], vertex[ 2 ] )
			self.__collision_node.addSolid( poly )
			triangleCount += 1
			print( self )
		self.__collision_node.setPythonTag( 'collision_target', self )
		self.__polygonPool.addPolygonToPool( self._name, self )

	@property
	def neighbors( self ):
		return self.__neighbors

	def randomNeighbor( self ):
		return random.choice( list( self.__neighbors.values() ) )

	@neighbors.setter
	def neighbors( self, neighbors ):
		self.__neighbors = neighbors

	def __assignEdges( self, vertices ):
		self.__edges[ Direction.UP_RIGHT ] = vertices[ 0 ][ 0 ]
		self.__edges[ Direction.UP_LEFT ] = vertices[ 0 ][ 1 ]
		self.__edges[ Direction.DOWN_RIGHT ] = vertices[ 1 ][ 1 ]
		self.__edges[ Direction.DOWN_LEFT ] = vertices[ 1 ][ 0 ]

	def showNeighbors( self, startRow: int, startCol: int, level: int ):
		row_diff = abs( self._row - startRow )
		col_diff = abs( self._col - startCol )

		if self._visible or abs( row_diff ) > level or abs( col_diff ) > level:
			return

		self.__displayFrameAndEdges( level, col_diff, row_diff, startCol, startRow )
		self._showDebugNode()
		self._colorDebugNode()
		self._visible = True
		for neighbor in self.__neighbors.values():
			neighbor.showNeighbors( startRow, startCol, level )

	def __displayFrameAndEdges( self, level: int, col_diff: int, row_diff: int, startCol: int, startRow: int ):
		if row_diff == level and col_diff == level:
			self.__showFrame()
			if self._row > startRow and self._col < startCol:  # Down
				self.__drawEdges( Direction.UP_LEFT, Direction.UP_RIGHT )
			elif self._row < startRow and self._col > startCol:  # Up left
				self.__drawEdges( Direction.DOWN_RIGHT, Direction.DOWN_LEFT )
			elif self._row > startRow and self._col > startCol:  # Up right
				self.__drawEdges( Direction.UP_LEFT, Direction.DOWN_LEFT )
			else:  # Down left
				self.__drawEdges( Direction.UP_RIGHT, Direction.DOWN_RIGHT )

		elif row_diff == level and col_diff < level:
			# Handle vertical edge cases
			if self._row > startRow:
				self.__drawEdges( Direction.UP_LEFT )
			elif self._row < startRow:
				self.__drawEdges( Direction.DOWN_RIGHT )

		elif row_diff < level and col_diff == level:
			# Handle horizontal edge cases
			if self._col > startCol:
				self.__drawEdges( Direction.DOWN_LEFT )
			elif self._col < startCol:
				self.__drawEdges( Direction.UP_RIGHT )

	def __showFrame( self, color = Vec4( 0, 1, 0, 0.5 ) ):
		self._wire_node_path.setColor( color )
		self._wire_node_path.show()

	def hideNeighbors( self ):
		if not self._visible:
			return

		self.__hideDebugNode()
		for neighbor in self.__neighbors.values():
			neighbor.hideNeighbors()

	def __hideDebugNode( self ):
		self._visible = False
		self._debug_node_path.hide()
		self._wire_node_path.hide()



	def __drawEdges( self, *args ):
		for direction in args:
			point = Point3( self.__edges[ direction ] )
			self.__draw_point( point, self.pointColor() )

	def __removeAllEdges( self ):
		for edge in currentFrame:
			edge.remove_node()
		currentFrame.clear()

	def __draw_point( self, point: Point3, color = Color.GREEN ):
		geom_node = getPointGeomNode( point )
		__point_node_path = self._child.attachNewNode( geom_node )
		__point_node_path.setZ( __point_node_path.getZ() + 0.02 )
		__point_node_path.set_render_mode_thickness( 5 )
		__point_node_path.setColor( color.value )
		currentFrame.append( __point_node_path )

	def attachCollisionNodeToTerrain( self ):
		self.__collision_node_path = self._child.attachNewNode( self.__collision_node )
		self._attachDebugNode( self.__collision_node )


	@classmethod
	def acquireAllNeighbors( cls ):
		CustomPolygonPool.Instance().acquireAllNeighbors()

	def pointColor( self ):
		if self._angle > 0.2:
			return Color.RED
		return Color.WHITE

	def handleSelection( self, mode: SelectionModes = SelectionModes.ANY ):
		if self.isSelected( mode ):
			return

		self._selectionMode = mode
		if mode == SelectionModes.CREATE:
			self.__markArea( level = 0, color = Color.BLUE.value )
		if mode == SelectionModes.P2P:
			self.__markArea( level = 0, color = Color.YELLOW.value )

	def handleSelectItem( self, item: 'SelectionItem' ) -> SelectionItem | None:
		item.handleSelection( SelectionModes.CREATE )
		self.clearSelection()
		return item

	def clearSelection( self ):
		self._selectionMode = SelectionModes.NONE
		self.__hideDebugNode()
		#self.hideNeighbors()

	def __markArea( self, level = 0, color = None ):
		self.__removeAllEdges()
		currentFrame.clear()
		self.hideNeighbors()
		self.showNeighbors( self._row, self._col, level )
		self._showDebugNode()
		self._colorDebugNode( color )

