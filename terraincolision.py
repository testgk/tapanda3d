from panda3d.core import GeoMipTerrain, GeomNode, NodePath

from customcollisionpolygon import CustomCollisionPolygon

polygons = {}

class TerrainCollision:
    def __init__( self, terrain: GeoMipTerrain, physicsWorld, render ):
        self.__terrain = terrain
        self.__physicsWorld = physicsWorld
        self.__render = render

    def createTerrainCollision( self ):
            root = self.__terrain.getRoot()
            for child in root.getChildren():
                terrainHeight = self.get_terrain_height( child.getX(), child.getY() )
                print( f'{ terrainHeight} ' )
                if isinstance( child.node(), GeomNode ):
                    customCollisionPolygon = CustomCollisionPolygon( child, terrainHeight )
                    customCollisionPolygon.attachCollisionNodeToTerrain()
                    customCollisionPolygon.attachRigidBodyNodeToTerrain( self.__render )
                    self.__physicsWorld.attachRigidBody( customCollisionPolygon.rigidBodyNode )
                    #customCollisionPolygon.updateTerrainPosition()
                    #rigid_body_np = self.__render.attachNewNode( customCollisionPolygon.rigidBodyNode )
                    #rigid_body_np.show()
            CustomCollisionPolygon.acquireAllNeighbors()


    def get_terrain_height(self, x, y):
        """Return the height of the terrain at a given (x, y) position."""
        return self.__terrain.getElevation(x, y) * 100

