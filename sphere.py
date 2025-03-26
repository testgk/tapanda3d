from panda3d.core import GeomVertexFormat, GeomVertexData, Geom, GeomVertexWriter, GeomTriangles, GeomNode
from panda3d.core import NodePath
from math import sin, cos, pi

from enums.colors import Color





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
