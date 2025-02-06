import random

from panda3d.bullet import BulletSphereShape, BulletRigidBodyNode
from panda3d.core import NurbsCurveEvaluator, Vec4, Vec3, LineSegs, NodePath

from enums.colors import Color
from sphere import create_sphere


class Curve:
	def __init__( self, world, render ):
		self.__render = render
		self.__world = world
		self.__curve = None
		self.__curve_np = None

	def createCurvePath( self, positions = list ):
		self.__curve = self.__createCurve( positions )
		self.__visualize_curve()
		self.__generateRandom()
		return self.__curve

	def __createCurve( self, positions ):
		if len( positions ) < 3:
			raise ValueError( "At least 3 positions are required to create a NURBS __curve." )
		curve_evaluator = NurbsCurveEvaluator()
		curve_evaluator.reset( len( positions ) )
		for i, pos in enumerate( positions ):
			curve_evaluator.set_vertex( i, Vec4( pos[ 0 ], pos[ 1 ], pos[ 2 ] + 100, 1 ) )
		curve_evaluator.set_order( 3 )
		return curve_evaluator.evaluate()

	def __visualize_curve( self, curve, num_samples: int = 100 ):
		if self.__curve_np:
			self.__curve_np.remove_node()

		lines = LineSegs()
		lines.set_thickness( 2.0 )
		pos = Vec3()

		for i in range( num_samples + 1 ):  # +1 to include the endpoint
			t = i / num_samples
			self.__curve.eval_point( t, pos )
			lines.draw_to( pos )

		self.__curve_np = NodePath( lines.create() )
		self.__curve_np.reparent_to( self.__render )


	def __generateRandom( self, numOfPoints: int = 10 ):
		for _ in range( numOfPoints ):
			t = random.uniform( 0.0, 1.0 )
			pos = Vec3()
			self.__curve.eval_point( t, pos )
			point = create_and_setup_rigid_sphere( self.__render, position = pos, color = Color.BLUE )
			self.__world.attach( point )
			if self.__world.contactTest( point, self.__curve.obstacle.coreRigidBody ).get_num_contacts() > 0:
				print( f"Curve touches model at t={ t } (Position: { pos })" )


def create_and_setup_rigid_sphere( parent, color, position, radius = 5.0, slices = 16, stacks = 8 ):
	shape = BulletSphereShape( radius )
	body = BulletRigidBodyNode( 'RigidSphere' )
	body.addShape( shape )
	body.setMass( 0.0 )
	body_np = parent.attachNewNode( body )
	body_np.setPos( position )
	sphere = create_sphere( radius = radius, color = color, slices = slices, stacks = stacks )
	sphere.reparentTo( body_np )
	return body