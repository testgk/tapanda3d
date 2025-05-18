from panda3d.bullet import BulletHeightfieldShape, BulletRigidBodyNode
from panda3d.core import Filename, GeoMipTerrain, PNMImage, Point3, BitMask32, Texture, NodePath


class TerrainInfo:
    def __init__( self, terrain ):
        self.terrain = terrain
        #self.__heightMap = heightMap
        self.__terrainSize = 2000
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
    def __init__( self, loader, render ):
        self._loader = loader
        self._render = render

    def create_terrain(self, terrainName: str, showTexture: bool, blockSize = 64 ) -> TerrainInfo:
        model = self._loader.loadModel( "/home/gadik@liveu.tv/pyprojects/tapanda/maps/rocky_terrain_02_1k.gltf" )
        model.reparentTo( self._render )

        #terrain = GeoMipTerrain( "terrain" )
        #heightmap = PNMImage( Filename( f"maps/{ terrainName }.png" ) )
        #terrain.setHeightfield( heightmap )
        #terrain.setBlockSize( blockSize )
        #terrain.setNear( 40 )
        #terrain.setFar( 200 )
        #terrain.getRoot().setSz( 100 )
        #terrain.generate()
        #if showTexture:
        #   texture = self._loader.loadTexture( "maps/rocky_terrain_diff_4k.jpg" )
        #    texture.setMinfilter( Texture.FTLinearMipmapLinear )
        #   texture.setMagfilter( Texture.FTLinear )
        #   terrain.getRoot().setTexture( texture )
        return TerrainInfo( model )

    def loadTerrainModel( self, terrainModelPath: str, showTexture: bool ) -> NodePath:
        terrain = self._loader.loadModel( terrainModelPath )
        terrain.reparentTo( self._render )

        if showTexture:
            texture = self._loader.loadTexture( "maps/rocky_terrain_diff_4k.jpg" )
            texture.setMinfilter( Texture.FTLinearMipmapLinear )
            texture.setMagfilter( Texture.FTLinear )
            terrain.setTexture( texture, 1 )

        return terrain