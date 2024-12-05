from panda3d.core import GeoMipTerrain, GeomNode, NodePath
from customrigidpolygon import CustomRigidPolygon


class TerrainRigidBody:
	def __init__( self, terrain: GeoMipTerrain, physicsWorld ):
		self.__terrain = terrain
		self.__physicsWorld = physicsWorld

	def createTerrainRigidBody( self ):
		root = self.__terrain.getRoot()
		for child in root.getChildren():
			if isinstance( child.node(), GeomNode ):
				customRigidPolygon = CustomRigidPolygon( child )
				customRigidPolygon.attachRigidBodyNodeToTerrain()
				self.__physicsWorld.attachRigidBody( customRigidPolygon.rigidBodyNode )


