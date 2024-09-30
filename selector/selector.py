from panda3d.bullet import BulletHelper, BulletRigidBodyNode, BulletTriangleMesh, BulletTriangleMeshShape
from panda3d.core import Vec3, Vec4, BitMask32
from camera import TerrainCamera
from entities.entity import Entity

class Selector:
	last_picked_entity = None

	def __init__( self, terrain, picker, mouseWatcherNode, camNode, terrainCamera: TerrainCamera, physicsWorld, render ):
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
		if self.last_picked_entity is not None:
			self.last_picked_entity.clearSelection()
		print( f"Clicked node: { picked_obj }" )
		picked_entity = picked_obj.node().getPythonTag( 'collision_target' )
		self.last_picked_entity = picked_entity
		print( f"Clicked entity: { picked_entity }" )
		picked_entity.handleSelection( "mouse1" )

	def on_map_loader_click( self, entity: Entity ):
		entry = self.__getNewEntry()
		if entry is None:
			return
		picked_obj = entry.getIntoNodePath()
		print( f"Clicked node: { picked_obj }" )
		custom_collision_polygon = picked_obj.node().getPythonTag( 'collision_target' )
		if custom_collision_polygon:
			custom_collision_polygon.showDebugNode()
			model_np = self.__render.attachNewNode( entity.rigidBodyNode )
			self.physicsWorld.attachRigidBody( entity.rigidBodyNode )
			model_np.set_pos( entry.getSurfacePoint( self.__render ) )
			model_np.setZ( model_np.getZ() + 50 )
			for models in entity.models:
				models.reparentTo( model_np )
			force = Vec3( 500, 0, 0 )
