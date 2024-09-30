from panda3d.bullet import BulletHelper, BulletRigidBodyNode, BulletTriangleMesh, BulletTriangleMeshShape
from panda3d.core import Vec3, Vec4, BitMask32

from camera import TerrainCamera
import customcollisionpolygon
from direct.showbase.ShowBase import ShowBase

from entities.entity import Entity
from enums.colors import Color
from phyisics import globalClock
from selector.entityselector import EntitySelector


class Selector:

	def __init__( self, terrain, picker, mouseWatcherNode, camNode, terrainCamera: TerrainCamera, physicsWorld, render ):
		self.__terrain = terrain
		self.__last_custom_collision_polygon = None
		self.__camNode = camNode
		self.__render = render
		self.__generalPicker = picker
		self.__mouseWatcherNode = mouseWatcherNode
		self.__terrainCamera = terrainCamera
		self.physicsWorld = physicsWorld
		self.__entitySelector = EntitySelector( terrain, picker, mouseWatcherNode, camNode, terrainCamera, render )

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
		print( f"point: { point }" )
		entry = self.__getNewEntry()
		if entry is None:
			return
		picked_obj = entry.getIntoNodePath()
		print( f"Clicked node: { picked_obj }" )
		picked_entity = picked_obj.node().getPythonTag( 'collision_target' )
