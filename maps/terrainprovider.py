from panda3d.bullet import BulletHeightfieldShape, BulletRigidBodyNode
from panda3d.core import Filename ,GeoMipTerrain ,PNMImage ,Point3 ,BitMask32 ,Texture


class TerrainInfo:
    def __init__( self, terrain: GeoMipTerrain, heightMap: PNMImage ):
        self.terrain = terrain
        self.__heightMap = heightMap
        self.__terrainSize = heightMap.getXSize()
        self.__terrainCenter = Point3( self.__terrainSize / 2, self.__terrainSize / 2, 0 )

    @property
    def terrainSize( self ):
        return self.__terrainSize

    @property
    def terrainCenter( self ) -> Point3:
        return self.__terrainCenter

    @property
    def heightMap( self ) -> PNMImage:
        return self.__heightMap



class TerrainProvider:
    def __init__( self, loader ):
        self._loader = loader

    def create_terrain(self, terrainName: str, showTexture: bool, blockSize = 128 ) -> TerrainInfo:
        terrain = GeoMipTerrain( "terrain" )
        heightmap = PNMImage( Filename( f"maps/{ terrainName }.png" ) )
        terrain.setHeightfield( heightmap )
        terrain.setBlockSize( blockSize )
        terrain.setNear( 40 )
        terrain.setFar( 200 )
        terrain.getRoot().setSz( 100 )
        terrain.generate()
        if showTexture:
            texture = self._loader.loadTexture( "maps/terrain_texture.png" )
            texture.setMinfilter( Texture.FTLinearMipmapLinear )
            texture.setMagfilter( Texture.FTLinear )
            terrain.getRoot().setTexture( texture )
        return TerrainInfo( terrain, heightmap )
