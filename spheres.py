from panda3d.core import GeomTriangles, GeomNode
from panda3d.core import NodePath
from math import sin, cos, pi

from enums.colors import Color

from panda3d.bullet import BulletSphereShape, BulletRigidBodyNode
from panda3d.core import GeomVertexFormat, GeomVertexData, GeomVertexWriter, Geom



def createAndSetupSphere( parent, color, position, radius = 5.0, slices = 16, stacks = 8 ):
	sphere = createSphere( radius = radius, slices = slices, stacks = stacks )
	sphere.reparentTo( parent )
	sphere.setColor( color )
	sphere.setPos( position )
	return sphere

def createAndSetupRigidSphere( parent, color, position, radius = 5.0, slices = 16, stacks = 8 ):
	sphere = createAndSetupSphere( parent, color, position, radius = radius, slices = slices, stacks = stacks )
	shape = BulletSphereShape( radius )
	body = BulletRigidBodyNode( 'RigidSphere' )
	body.addShape( shape )
	body.setMass( 1.0 )
	body_np = parent.attachNewNode( body )
	body_np.setPos( position )
	sphere.reparentTo( body_np )
	return body_np

def createSphere( radius = 1.0, slices = 16, stacks = 16, color = Color.RED ):
	# Set up the vertex format
	format = GeomVertexFormat.get_v3n3()
	vdata = GeomVertexData( "sphere", format, Geom.UH_static )
	vdata.setNumRows( (slices + 1) * (stacks + 1) )

	vertex = GeomVertexWriter( vdata, "vertex" )
	normal = GeomVertexWriter( vdata, "normal" )

	# Generate vertices
	for stack in range( stacks + 1 ):
		phi = pi * stack / stacks
		for slice in range( slices + 1 ):
			theta = 2 * pi * slice / slices
			x = radius * sin( phi ) * cos( theta )
			y = radius * sin( phi ) * sin( theta )
			z = radius * cos( phi )
			vertex.addData3( x, y, z )
			normal.addData3( x / radius, y / radius, z / radius )  # Normalized normal

	# Generate triangles
	geom = Geom( vdata )
	tris = GeomTriangles( Geom.UH_static )
	for stack in range( stacks ):
		for slice in range( slices ):
			idx1 = stack * (slices + 1) + slice
			idx2 = idx1 + 1
			idx3 = idx1 + (slices + 1)
			idx4 = idx3 + 1

			tris.addVertices( idx1, idx2, idx3 )
			tris.addVertices( idx2, idx4, idx3 )

	geom.addPrimitive( tris )

	# Create a GeomNode to hold the geometry
	node = GeomNode( "sphere" )
	node.addGeom( geom )
	np = NodePath( node )
	np.setColor( color )
	return np
