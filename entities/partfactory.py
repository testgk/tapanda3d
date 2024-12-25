import os
import random
from collections import defaultdict
from typing import TYPE_CHECKING, Callable
from panda3d.core import  NodePath, Vec3, CollisionBox, CollisionNode, Point3
from panda3d.bullet import BulletRigidBodyNode, BulletTriangleMesh, BulletTriangleMeshShape


if TYPE_CHECKING:
    from entities.entity import Entity
    from entities.parts.part import Part

from objects.stltoeggconverter import convert_stl_to_egg


def find_entity_parts( cls ) -> list[ Callable ]:
    entityParts = [ ]
    for name in dir( cls ):
        attr = getattr( cls, name )
        if getattr( attr, '_is_entitypart', False ):
            entityParts.append( attr )
    return entityParts


class PartFactory:
    def __init__( self, entity: 'Entity' ):
        self.__dimensions = None
        self.__entity = entity
        self.__models = []
        self.__collisionBox = None
        self.__rigidBodiesInfo = { }
        self.__parts: list[ 'Part' ] = [ ]
        self.__modelData = defaultdict( list )
        self.__rigidBodyNodes = []


    def addParts( self ) -> list[ 'Part' ]:
        parts = find_entity_parts( self.__entity )
        for part in parts:
            self.__parts.append( part() )
        return self.__parts

    @property
    def collisionBox( self ) -> NodePath:
        return self.__collisionBox

    @property
    def rigidBodies( self ) -> dict:
        return self.__rigidBodiesInfo

    @property
    def rigidBodyNodes( self ):
        return self.__rigidBodyNodes

    @property
    def models( self ) -> list[ NodePath ]:
        return self.__models

    def build( self, loader ):
        self.addParts()
        self.createModels( loader )
        self.createCollisionBox()
        self.createRigidBodies()

    def createModels( self, loader ) -> None:
        for part in self.__parts:
            try:
                eggPath = self.__getPartEggPath( part )
                model = self.__loadModel( eggPath, loader, part )
                model.setScale( self.__entity.scale )
                self.__models.append( model )
                part.model = model
            except Exception as e:
                print( e )

    def __loadModel( self, eggPath: super, loader, part: 'Part' ) -> NodePath:
        model = loader.loadModel( eggPath )
        model.setColor( part.color )
        model.setPythonTag( 'model_part', part )
        return model

    def __getPartEggPath( self, part: 'Part' ):
        fullPath = os.path.join( "objects/parts/", part.objectPath, part.partId )
        eggPath = fullPath + ".egg"
        if os.path.exists( eggPath ):
            return eggPath

        stlPath = fullPath + ".stl"
        if os.path.exists( stlPath ):
            convert_stl_to_egg( stlPath, eggPath )
            return eggPath

    def createCollisionBox( self ):
        self.__dimensions, collision_box_node = create_combined_collision_box( self.__models )
        self.__collisionBox = self.__parts[ 0 ].model.attachNewNode( collision_box_node )

    def createRigidBodies( self ) -> None:
        modelData = defaultdict( list )
        for part in self.__parts:
            modelData[ part.rigidGroup ].append( part )

        for rg, parts in modelData.items():
            models = [ p.model for p in parts ]
            body_node = self.__createSingleRigidBody( models )
            body_node.setPythonTag( 'raytest_target', self.__entity )
            self.__rigidBodyNodes.append( body_node )
            self.__rigidBodiesInfo[ rg ] = { "rigidbody": body_node, "parts": parts }

    def __createSingleRigidBody( self, models: list ) -> BulletRigidBodyNode:
        body_node = BulletRigidBodyNode( f'multi_shape_body_{random.randint(1,1000)}' )
        for model in models:
            mesh = BulletTriangleMesh()
            add_model_to_bullet_mesh( mesh, model )
            model_shape = BulletTriangleMeshShape( mesh, dynamic = True )
            body_node.addShape( model_shape )
            part = model.getPythonTag( 'model_part' )
            part.setRigidBodyProperties( body_node )
        return body_node


def get_model_dimensions( model_np ) -> ( Vec3, Vec3 ):
    geom_node = model_np.find( "**/+GeomNode" ).node()
    if not geom_node:
        return None

    min_bounds = Vec3( float( 'inf' ), float( 'inf' ), float( 'inf' ) )
    max_bounds = Vec3( float( '-inf' ), float( '-inf' ), float( '-inf' ) )

    for i in range( geom_node.getNumGeoms() ):
        geom = geom_node.getGeom( i )
        bounds = geom.getBounds()
        min_bounds.setX( min( min_bounds.x, bounds.getMin().x ) )
        min_bounds.setY( min( min_bounds.y, bounds.getMin().y ) )
        min_bounds.setZ( min( min_bounds.z, bounds.getMin().z ) )
        max_bounds.setX( max( max_bounds.x, bounds.getMax().x ) )
        max_bounds.setY( max( max_bounds.y, bounds.getMax().y ) )
        max_bounds.setZ( max( max_bounds.z, bounds.getMax().z ) )
    return min_bounds, max_bounds


def create_combined_collision_box( model_nps ):
    if not model_nps:
        return None

    # Initialize min and max bounds to extreme values
    min_bounds = Point3(float('inf'), float('inf'), float('inf'))
    max_bounds = Point3(float('-inf'), float('-inf'), float('-inf'))

    # Iterate through each model to determine the overall bounds
    for model_np in model_nps:
        dimensions = get_model_dimensions(model_np)
        if dimensions is None:
            continue

        model_min, model_max = dimensions
        min_bounds.x = min(min_bounds.x, model_min.x)
        min_bounds.y = min(min_bounds.y, model_min.y)
        min_bounds.z = min(min_bounds.z, model_min.z)
        max_bounds.x = max(max_bounds.x, model_max.x)
        max_bounds.y = max(max_bounds.y, model_max.y)
        max_bounds.z = max(max_bounds.z, model_max.z)

    # Calculate dimensions of the combined bounding box
    width = max_bounds.x - min_bounds.x
    height = max_bounds.y - min_bounds.y
    depth = max_bounds.z - min_bounds.z

    # Calculate center of the combined bounding box
    center_x = (min_bounds.x + max_bounds.x) / 2
    center_y = (min_bounds.y + max_bounds.y) / 2
    center_z = (min_bounds.z + max_bounds.z) / 2

    # Create the collision box
    collision_box = CollisionBox(
        Vec3(center_x, center_y, center_z),  # Center of the box
        width / 2, height / 2, depth / 2    # Half extents
    )

    # Add collision box to a collision node
    collision_node = CollisionNode('combined_model_collision')
    collision_node.addSolid(collision_box)

    return ( width, height, depth ), collision_node


def add_model_to_bullet_mesh( mesh, model_np ):
    geom_node = model_np.find( "**/+GeomNode" ).node()
    for i in range( geom_node.getNumGeoms() ):
        geom = geom_node.getGeom( i )
        mesh.addGeom( geom )
