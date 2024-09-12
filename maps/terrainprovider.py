from panda3d.core import Filename, GeoMipTerrain, PNMImage, Point3


class TerrainInfo:
    def __init__( self, terrain: GeoMipTerrain, heightMap: PNMImage ):
        self.terrain = terrain
        self.heightMap = heightMap
        self.__terrainSize = heightMap.getXSize()
        self.__terrainCenter = Point3( self.__terrainSize / 2, self.__terrainSize / 2, 0 )

    @property
    def terrainSize( self ):
        return self.__terrainSize

    @property
    def terrainCenter( self ) -> Point3:
        return self.__terrainCenter


class TerrainProvider:
    def __init__( self, loader ):
        self._loader = loader

    def create_terrain(self, terrainName: str ) -> TerrainInfo:
        terrain = GeoMipTerrain( "terrain" )
        heightmap = PNMImage( Filename( f"maps/{ terrainName }.png" ) )
        terrain.setHeightfield( heightmap )
        # Set terrain properties
        terrain.setBlockSize( 16 )
        terrain.setNear( 40 )
        terrain.setFar( 200 )
        terrain.getRoot().setSz( 100 )
        terrain.generate()
        texture = self._loader.loadTexture( "maps/terrain_texture.png" )
        terrain.getRoot().setTexture( texture )
        return TerrainInfo( terrain, heightmap )
