from panda3d.bullet import BulletSphereShape, BulletRigidBodyNode
from panda3d.core import NurbsCurveEvaluator, Vec4, Vec3, LineSegs, NodePath

from enums.colors import Color
from spheres import createSphere
from target import CustomTarget


class CurveGenerator:
	def __init__( self, world, render ):
		self.__rigidPoints = []
		self.__render = render
		self.__world = world
		self.__curve = None
		self.__curve_np = None
		self.__curvePositions = []

	def getCurveTargets( self ) -> list:
		return [ CustomTarget( position = position ) for position in reversed( self.__curvePositions ) ]

	def generateNewCurve( self, positions = list ):
		self.__curve = self.__createCurve( positions )
		self.__visualizeCurve()
		return self.__curve

	def terminateCurve( self ):
		self.__curve = None
		if self.__curve_np:
			self.__curve_np.remove_node()
		#	self.__curve_np = None
		#self.__clearRigidPoints()
		#self.__curvePositions.clear()
		#self.__rigidPoints.clear()

	def __createCurve( self, positions ):
		if self.__curve_np:
			self.__curve_np.remove_node()
		self.__curvePositions.clear()
		curve_evaluator = NurbsCurveEvaluator()
		curve_evaluator.reset( len( positions ) )
		for i, pos in enumerate( positions ):
			curve_evaluator.set_vertex( i, Vec4( pos[ 0 ], pos[ 1 ], pos[ 2 ] + 100, 1 ) )
		curve_evaluator.set_order( 3 )
		return curve_evaluator.evaluate()

	def __visualizeCurve( self, num_samples: int = 100 ):
		print( "visualizing curve" )
		lines = LineSegs()
		lines.set_thickness( 2.0 )
		pos = Vec3()
		for i in range( num_samples + 1 ):  # +1 to include the endpoint
			t = i / num_samples
			self.__curve.eval_point( t, pos )
			lines.draw_to( pos )

		self.__curve_np = NodePath( lines.create() )
		self.__curve_np.reparent_to( self.__render )

	def checkCurveObstacleContact( self, curve, obstacle, numOfPoints: int = 100 ):
		for i in range( numOfPoints ):
			point = None
			sphere = None
			try:
				t = i / (numOfPoints - 1)  # Evenly spaced t values
				pos = Vec3()
				curve.eval_point( t, pos )
				point, sphere = createRigidPoint( self.__render, position = pos, color = Color.BLUE )
				self.__world.attach( point )
				#self.__rigidPoints.append( point )

				if self.__world.contactTest( point, obstacle.coreRigidBody ).get_num_contacts() > 0:
					print( f"Curve touches model at t={ t } ( Position: { pos } )" )
					return False

				self.__curvePositions.append( pos )
			finally:
				sphere.removeNode()
				self.__world.removeRigidBody( point )
		return True

def createRigidPoint( parent, color, position, radius = 5.0, slices = 16, stacks = 8 ):
	shape = BulletSphereShape( radius )
	body = BulletRigidBodyNode( 'RigidSphere' )
	body.addShape( shape )
	body.setMass( 0.0 )
	body_np = parent.attachNewNode( body )
	body_np.setPos( position )
	sphere = createSphere( radius = radius, color = color, slices = slices, stacks = stacks )
	sphere.reparentTo( body_np )
	return body, body_np