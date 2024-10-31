from camera import TerrainCamera
from entities.entity import Entity
from entities.mover import Mover


class Selector:
	last_picked_entity = None

	@property
	def selectedEntity( self ) -> Mover:
		return self.last_picked_entity

	@property
	def entry( self ):
		return self.__entry

	def __init__( self, terrain, picker, mouseWatcherNode, camNode, terrainCamera: TerrainCamera, physicsWorld, render ):
		self.__entry = None
		self.__terrain = terrain
		self.__last_custom_collision_polygon = None
		self.__camNode = camNode
		self.__render = render
		self.__generalPicker = picker
		self.__mouseWatcherNode = mouseWatcherNode
		self.__terrainCamera = terrainCamera
		self.physicsWorld = physicsWorld

	def __getNewEntry( self ):
		if self.__mouseWatcherNode.hasMouse():
			mousePosition = self.__mouseWatcherNode.getMouse()
			self.__generalPicker.pickerRay.setFromLens( self.__camNode, mousePosition.getX(), mousePosition.getY() )
			self.__generalPicker.picker.traverse( self.__render )
			numEntries = self.__generalPicker.pickerQueue.getNumEntries()
			if numEntries > 0:
				self.__generalPicker.pickerQueue.sortEntries()
				entry = self.__generalPicker.pickerQueue.getEntry( 0 )
				return entry

	def on_map_click( self ):
		entry = self.__getNewEntry()
		if entry is None:
			return
		point = entry.getSurfacePoint( self.__render )
		self.__terrainCamera.setCenter( point )
		print( f"point: { point }" )
		picked_obj = entry.getIntoNodePath()
		if picked_obj is None:
			return
		self.__entry = entry
		if self.last_picked_entity is not None:
			self.last_picked_entity.clearSelection()
		print( f"Clicked node: { picked_obj }" )
		picked_entity = picked_obj.node().getPythonTag( 'collision_target' )
		self.last_picked_entity = picked_entity
		print( f"Clicked entity: { picked_entity }" )
		picked_entity.handleSelection( "mouse1" )
