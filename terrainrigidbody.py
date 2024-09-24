from panda3d.core import GeoMipTerrain, GeomNode, NodePath

from customcollisionpolygon import CustomCollisionPolygon
from customrigidpolygon import CustomRigidPolygon


class TerrainRigidBody:
	def __init__( self, terrain: GeoMipTerrain, physicsWorld, render ):
		self.__terrain = terrain
		self.__physicsWorld = physicsWorld
		self.__render = render

	def createTerrainRigidBody( self ):
		root = self.__terrain.getRoot()
		for child in root.getChildren():
			terrainHeight = self.get_terrain_height( child.getX(), child.getY() )
			print( f'{terrainHeight} ' )
			if isinstance( child.node(), GeomNode ):
				customRigidPollygon = CustomRigidPolygon( child )
				customRigidPollygon.attachRigidBodyNodeToTerrain()
				self.__physicsWorld.attachRigidBody( customRigidPollygon.rigidBodyNode )
		CustomCollisionPolygon.acquireAllNeighbors()

	def get_terrain_height( self, x, y ):
		"""Return the height of the terrain at a given (x, y) position."""
		return self.__terrain.getElevation( x, y ) * 100
