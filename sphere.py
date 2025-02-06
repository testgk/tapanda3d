from panda3d.core import GeomVertexFormat, GeomVertexData, Geom, GeomVertexWriter, GeomTriangles, GeomNode
from panda3d.core import NodePath
from math import sin, cos, pi

from enums.colors import Color


def create_sphere( radius = 1.0, slices = 16, stacks = 16, color = Color.RED ):
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


# Initialize Panda3D and add the sphere to the scene
from direct.showbase.ShowBase import ShowBase


class MyApp( ShowBase ):
	def __init__( self ):
		super().__init__()
		# Create the sphere and attach it to the render tree
		sphere = create_sphere( radius = 1.0, slices = 32, stacks = 16 )
		sphere.reparentTo( self.render )
		sphere.setPos( 0, 10, 0 )  # Position the sphere
		sphere.setColor( 1, 0, 0, 1 )  # Set its color to red
