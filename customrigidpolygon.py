import math
from typing import Any

from panda3d.bullet import BulletConvexHullShape, BulletRigidBodyNode
from panda3d.core import BitMask32, CollisionNode, CollisionPolygon, DirectionalLight, GeomVertexReader, LVector4, \
    NodePath, Vec3, \
    GeomVertexFormat, GeomVertexData, GeomVertexWriter, GeomTriangles, Geom, GeomNode, Vec4, Point3, GeomLines, \
    GeomPoints

from collsiongroups import CollisionGroup
from enums.colors import Color
from enums.directions import Direction, mapDirections
from selector.selector import Selector


def getVertices( geom: GeomNode ) -> list:
    all_vertices = [ ]
    tris = geom.getPrimitive( 0 )  # Assuming the first primitive is triangles
    tris = tris.decompose()
    vertex_data = geom.getVertexData()
    vertex_reader = GeomVertexReader( vertex_data, 'vertex' )
    primitives = tris.getNumPrimitives()
    for i in range( tris.getNumPrimitives() ):
        prim_start = tris.getPrimitiveStart( i )
        prim_end = tris.getPrimitiveEnd( i )
        assert prim_end - prim_start == 3

        vertices = [ ]
        for pr_index in range( prim_start, prim_end ):
            vi = tris.getVertex( pr_index )
            vertex_reader.setRow( vi )
            v = vertex_reader.getData3()
            vertices.append( v )
        all_vertices.append( vertices )
    return all_vertices


class CustomRigidPolygon:
    def __init__( self, child: NodePath, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.__child = child
        self.__rigid_body_node_path = None
        self.__rigid_body_node = None
        self.__geom = child.node().getGeom( 0 )  # Assuming each GeomNode has one Geom
        self.__vertices = getVertices( self.__geom )

    @property
    def rigidBodyNode( self ) -> BulletRigidBodyNode:
        return self.__rigid_body_node

    def attachRigidBodyNodeToTerrain( self ):
        self.__rigid_body_node = create_convex_hull_rigid_body( self.__vertices )
        self.__rigid_body_node.setIntoCollideMask( CollisionGroup.MODEL | CollisionGroup.ROLLS )
        self.__rigid_body_node.setMass( 0 )
        self.__rigid_body_node_path = self.__child.attachNewNode( self.__rigid_body_node )

def create_convex_hull_rigid_body( vertices_list: list ) -> BulletRigidBodyNode:
    shape = BulletConvexHullShape()

    for triangle in vertices_list:
        for vertex in triangle:
            shape.addPoint( vertex )

    rigid_body_node = BulletRigidBodyNode( 'ConvexHullRigidBody' )
    rigid_body_node.addShape( shape )
    rigid_body_node.setMass( 0 )  # Set a non-zero mass for dynamic objects
    return rigid_body_node
