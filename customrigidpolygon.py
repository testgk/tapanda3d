import math
from typing import Any

from panda3d.bullet import BulletConvexHullShape, BulletRigidBodyNode, BulletDebugNode
from panda3d.core import BitMask32, CollisionNode, CollisionPolygon, DirectionalLight, GeomVertexReader, LVector4, \
    NodePath, Vec3, \
    GeomVertexFormat, GeomVertexData, GeomVertexWriter, GeomTriangles, Geom, GeomNode, Vec4, Point3, GeomLines, \
    GeomPoints

from collsiongroups import CollisionGroup
from custompolygon import CustomPolygon, getVertices
from enums.colors import Color
from enums.directions import Direction, mapDirections
from selector.selector import Selector





class CustomRigidPolygon( CustomPolygon ):
    def __init__( self, child: NodePath, *args, **kwargs ):
        super().__init__( child )
        self.__debugNode = None
        self._debug_node_path = None
        self.__rigid_body_node_path = None
        self.__rigid_body_node = None

    @property
    def rigidBodyNode( self ) -> BulletRigidBodyNode:
        return self.__rigid_body_node

    def attachRigidBodyNodeToTerrain( self ):
        self.__rigid_body_node = create_convex_hull_rigid_body( self._vertices )
        self.__rigid_body_node.setIntoCollideMask( CollisionGroup.MODEL | CollisionGroup.ROLLS )
        self.__rigid_body_node.setMass( 0 )
        self.__rigid_body_node_path = self._child.attachNewNode( self.__rigid_body_node )

    def _createTempDebug( self ):
        debugNode = BulletDebugNode( 'DebugSpecific' )
        debugNode.showWireframe( True )
        self._child.attachNewNode( self.__debugNode )
        self._debug_node_path = self._child.attachNewNode( self.__debugNode )
        self._debug_node_path.setZ( self._debug_node_path.getZ() + 10 )
        self._debug_node_path.setColor( Color.BLACK.value )
        self._debug_node_path.show()
        self.__rigid_body_node.setPythonTag( 'raytest_target', self )

    def show( self, world ):
        self._debug_node_path.show()

def create_convex_hull_rigid_body( vertices_list: list ) -> BulletRigidBodyNode:
    shape = BulletConvexHullShape()
    for triangle in vertices_list:
        for vertex in triangle:
            shape.addPoint( vertex )

    rigid_body_node = BulletRigidBodyNode( 'ConvexHullRigidBody' )
    rigid_body_node.addShape( shape )
    rigid_body_node.setMass( 0 )  # Set a non-zero mass for dynamic objects
    return rigid_body_node
