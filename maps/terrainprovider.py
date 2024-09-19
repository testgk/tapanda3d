from panda3d.bullet import BulletHeightfieldShape, BulletRigidBodyNode
from panda3d.core import Filename ,GeoMipTerrain ,PNMImage ,Point3 ,BitMask32


class TerrainInfo:
    def __init__( self, terrain: GeoMipTerrain, heightMap: PNMImage, rigidBodyNode: BulletRigidBodyNode ):
        self.terrain = terrain
        self.__heightMap = heightMap
        self.__terrainSize = heightMap.getXSize()
        self.__rigidBodyNode = rigidBodyNode
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

    @property
    def rigidBodyNode( self ) -> BulletRigidBodyNode:
        return self.__rigidBodyNode



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
        terrain.getRoot().setCollideMask( BitMask32.bit( 1 ) )
        terrain.generate()
        #texture = self._loader.loadTexture( "maps/terrain_texture.png" )
        #terrain.getRoot().setTexture( texture )
        rigidBodyNode = self.__terrainRigidBodyNode( heightmap )
        return TerrainInfo( terrain, heightmap, rigidBodyNode )

    def __terrainRigidBodyNode( self, heightMap ) -> BulletRigidBodyNode:
        max_height = 10  # Scale of the terrain's height
        up_axis = 2  # '2' represents Z-axis up
        heightfield_shape = BulletHeightfieldShape( heightMap, max_height, up_axis )
        rigid_node = BulletRigidBodyNode( 'Terrain' )
        rigid_node.addShape( heightfield_shape )
        rigid_node.setMass( 0 )  # Static body (non-movable)
        return rigid_node
        #terrain_np = self.render.attachNewNode(terrain_node)
        #terrain_np.setPos(0, 0, 0)
        #self.physics_world = BulletWorld()
        #self.physics_world.attachRigidBody( terrain_node )

