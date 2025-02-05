import math
import random
from distutils.command.sdist import sdist

from direct import task
from direct.directutil.Mopath import Mopath
from panda3d.core import LineSegs, NodePath, Vec3, NurbsCurveEvaluator, Vec4

from enums.colors import Color
from movement.detection import Detection
from phyisics import globalClock
from typing import TYPE_CHECKING

from sphere import create_sphere
from target import Target

if TYPE_CHECKING:
	from entities.full.movers.mover import Mover


class MovementManager:
	def __init__( self, entity, world ):
		self.__curve_np = None
		self.__curve = None
		self.__t = 0.0
		self.__detection = Detection( entity, world )
		self.__tempTarget = None
		self.__mover: Mover = entity
		self.aligned = False

	def set_velocity_toward_point_with_stop( self, task ):
		if not self.__mover.currentTarget:
			return task.cont
		speed = self.__mover.speed
		target_pos = self.__mover.currentTarget.position
		stop_threshold = 20
		#if self.__mover.hasObstacles():
		#	self.__mover.currentTarget.clearSelection()
		#	return task.done
		current_pos = self.__mover.position
		direction = Vec3( target_pos.x - current_pos.x, target_pos.y - current_pos.y, 0 )
		distance = direction.length()
		if distance < stop_threshold:
			self.__mover.coreRigidBody.set_linear_velocity( Vec3( 0, 0, 0 ) )
			self.__mover.clearCurrentTarget()
			return task.done
		direction.normalize()
		velocity = direction * speed
		self.__mover.coreRigidBody.set_linear_velocity( velocity )
		return task.cont

	def set_velocity_backwards_direction( self, task ):
		if not self.__mover.closeToObstacle():
			return task.done

		direction = Vec3( self.__mover.obstacle.position - self.__mover.position )
		direction.normalize()
		self.__mover.coreRigidBody.set_linear_velocity( direction * self.__mover.speed )
		return task.cont

	def createCurvePath( self, positions = list, targets: int = 5 ):
		self.__curve = self.__createCurve( positions )
		self.visualize_curve( self.__curve )
		self.__generateRandom( )
		#self.__generateRandom( __curve, targets )
		return self.__curve

	def visualize_curve( self, curve, num_samples: int = 100 ):
		if self.__curve_np:
			self.__curve_np.remove_node()

		lines = LineSegs()
		lines.set_thickness( 2.0 )
		pos = Vec3()

		for i in range( num_samples + 1 ):  # +1 to include the endpoint
			t = i / num_samples
			curve.eval_point( t, pos )
			lines.draw_to( pos )

		self.__curve_np = NodePath( lines.create() )
		self.__curve_np.reparent_to( self.__mover.render )


	def __createCurve( self, positions ):
		if len( positions ) < 3:
			raise ValueError( "At least 3 positions are required to create a NURBS __curve." )
		curve_evaluator = NurbsCurveEvaluator()
		curve_evaluator.reset( len( positions ) )
		for i, pos in enumerate( positions ):
			curve_evaluator.set_vertex( i, Vec4( pos[ 0 ], pos[ 1 ], pos[ 2 ] + 100, 1 ) )
		curve_evaluator.set_order( 3 )
		return curve_evaluator.evaluate()

	def moveAlogCurve( self, task ):
		if self.__t > 1.0:
			return task.done

		pos = Vec3()
		self.__curve.eval_point( self.__t, pos )  # Evaluate position
		self.__mover.setPos( pos )  # Move the object
		self.__t += self.__mover.speed * globalClock.get_dt()  # Increase __t over time
		return task.cont  # Continue updating

	def __generateRandom( self, numOfPoints: int = 10 ):
		for _ in range( numOfPoints ):
			t = random.uniform( 0.0, 1.0 )
			pos = Vec3()
			self.__curve.eval_point( t, pos )
			self.__renderPoint( pos )

	def __renderPoint( self, pos ):
		point = create_and_setup_sphere( self.__mover.render, position = pos, color = Color.RED )

	def distance_from_obstacle( self ):
		distance = ( self.__mover.obstacle.position - self.__mover.position ).length()
		print( "distance_from_obstacle:", distance )
		return distance

	def track_target_coreBody_angle( self, task ):
		if self.__mover.currentTarget is None:
			return task.cont
		h_diff, new_hpr = self.__getRelativeHpr( self.__mover.coreBodyPath, self.__mover.currentTarget.position,
		                                         tracking_speed = 50 )
		self.__mover.coreBodyPath.setHpr( new_hpr )
		if abs( h_diff ) <= 50:
			self.aligned = True
		else:
			self.aligned = False
		return task.cont

	def __getRelativeHpr( self, bodyPart, target_position, tracking_speed = 100 ):
		current_pos = bodyPart.getPos()
		current_hpr = Vec3( bodyPart.getHpr() )
		direction_vector = target_position - current_pos
		target_heading = math.degrees( math.atan2( direction_vector.y, direction_vector.x ) )
		target_hpr = Vec3( target_heading, 0, 0 )
		h_diff = target_hpr.x - current_hpr.x
		h_diff = ( h_diff + 180 ) % 360 - 180
		h_adjust = max( -tracking_speed * globalClock.getDt(), min( h_diff, tracking_speed * globalClock.getDt() ) )
		new_hpr = current_hpr + Vec3( h_adjust, 0, 0 )
		return h_diff, new_hpr

	def maintain_turret_angle( self, task ):
		if self.__mover.finishedMovement():
			return task.done
		h_diff, new_hpr = self.__getRelativeHpr( self.__mover.turretBase().rigidBodyPath, self.__getCurrentTarget().position, tracking_speed = 25 )
		self.__mover.turretBase().rigidBodyPath.setHpr( new_hpr )
		return task.cont

	def maintain_terrain_boundaries( self, terrainSize, task ):
		current_pos = self.__mover.coreBodyPath.get_pos()
		if current_pos.x <= 10:
			self.__mover.coreBodyPath.setPos( Vec3( 11, current_pos.y, current_pos.z ) )
			return task.cont
		elif current_pos.x >= terrainSize - 10:
			self.__mover.coreBodyPath.setPos( Vec3( terrainSize - 9, current_pos.y, current_pos.z ) )
		if current_pos.y <= 10:
			self.__mover.coreBodyPath.setPos( Vec3( current_pos.x, 11, current_pos.z ) )
			return task.cont
		elif current_pos.y >= terrainSize - 10:
			self.__mover.coreBodyPath.setPos( Vec3( current_pos.x, terrainSize - 9, current_pos.z ) )
		return task.cont

	def monitor_obstacles( self, task ):
		#task.delayTime = 0.5
		if self.__mover.obstacle is not None:
			return task.cont
		if self.__mover.currentTarget is None:
			return task.again
		obstacle = self.__checkForObstacles( self.__getCurrentTarget() )
		try:
			if obstacle is None:
				if self.__mover.obstacle is not None:
					self.__mover.obstacle.clearSelection()
					self.__mover.obstacle = obstacle
				return task.again
			return task.done
		finally:
			if obstacle is not None:
				print( "monitor_obstacles:", obstacle.detection )
			self.__mover.obstacle = obstacle

	def __checkForObstacles( self, target ):
		return self.__detection.detectObstacle( target )

	def target_detection( self, task ):
		if not self.__mover.hasObstacles():
			self.__mover.bpTarget = self.__tempTarget
			print( f'current random target: { self.__tempTarget }' )
			self.__tempTarget = None
			return task.done
		self.__tempTarget = self.__detection.detectPosition( target = self.__getCurrentTarget() )
		if self.__tempTarget:
			self.__mover.obstacle.clearSelection()
			self.__mover.obstacle = None
		return task.cont

	def __getCurrentTarget( self ):
		return self.__tempTarget or self.__mover.currentTarget

def create_and_setup_sphere( parent, color, position, radius = 5.0, slices = 16, stacks = 8 ):
	sphere = create_sphere( radius = radius, slices = slices, stacks = stacks )
	sphere.reparentTo( parent )
	sphere.setColor( color )
	sphere.setPos( position )
	return sphere