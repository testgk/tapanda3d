from panda3d.core import GeoMipTerrain, GeomNode

from customcollisionpolygon import CustomCollisionPolygon

polygons = {}

class TerrainCollision:
    def __init__( self, terrain: GeoMipTerrain ):
        self.terrain = terrain

    def createTerrainCollision( self ):
        root = self.terrain.getRoot()
        for child in root.getChildren():
            if isinstance( child.node(), GeomNode ):
                customCollisionPolygon = CustomCollisionPolygon( child )
                customCollisionPolygon.attachCollisionNodeToTerrain()

        CustomCollisionPolygon.acquireAllNeighbors()


