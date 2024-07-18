from panda3d.core import GeoMipTerrain, GeomNode, NodePath

from customcollisionpolygon import CustomCollisionPolygon

polygons = {}

class TerrainCollision:
    def __init__( self, terrain: GeoMipTerrain ):
        self.__terrain = terrain

    def createTerrainCollision( self ):
            root = self.__terrain.getRoot()
            for child in root.getChildren():
                terrainHeight = self.get_terrain_height( child.getX(), child.getY() )
                print( f'{ terrainHeight} ' )
                if isinstance( child.node(), GeomNode ):
                    customCollisionPolygon = CustomCollisionPolygon( child, terrainHeight )
                    customCollisionPolygon.attachCollisionNodeToTerrain()
                    customCollisionPolygon.updateTerrainPosition()

            CustomCollisionPolygon.acquireAllNeighbors()


    def get_terrain_height(self, x, y):
        """Return the height of the terrain at a given (x, y) position."""
        return self.__terrain.getElevation(x, y) * 100