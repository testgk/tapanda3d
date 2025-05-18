from panda3d.core import GeoMipTerrain, GeomNode
from polygons.customrigidpolygon import CustomRigidPolygon


class TerrainRigidBody:
	def __init__( self, terrain: GeoMipTerrain, physicsWorld, render ):
		self.__terrain = terrain
		self.__physicsWorld = physicsWorld
		self.__render = render

	def createTerrainRigidBody( self ):
		root = self.__terrain
		for child in root.getChildren():
			if isinstance( child.node(), GeomNode ):
				customRigidPolygon = CustomRigidPolygon( child )
				customRigidPolygon.attachRigidBodyNodeToTerrain()
				customRigidPolygon.createAndRenderDebugNode( self.__render, self.__terrain.getElevation( child.getX(), child.getY() ) * 100 )
				self.__physicsWorld.attachRigidBody( customRigidPolygon.rigidBodyNode )


	def get_terrain_height( self, x, y ):
		"""Return the height of the terrain at a given (x, y) position."""
		return self.__terrain.getElevation( x, y ) * 100