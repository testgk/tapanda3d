
import math
from panda3d.core import Vec3

from movement.curve import CurveGenerator
from movement.pathdetector import PathDetector
from phyisics import globalClock
from typing import TYPE_CHECKING

from target import CustomTarget

if TYPE_CHECKING:
	from entities.full.movers.mover import Mover


class MovementManager:
	def __init__( self, entity, world, render ):
		self.__detector = PathDetector( entity, world, render )
		self._curveGenerator = CurveGenerator( world, render )
		self.__tempTarget = None
		self.__mover: Mover = entity

	def set_velocity_toward_point_with_stop( self, task ):
		if not self.__mover.currentTarget:
			return task.cont
		speed = self.__mover.speed
		target_pos = self.__mover.currentTarget.position
		stop_threshold = 20
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

	def distance_from_obstacle( self ):
		distance = ( self.__mover.obstacle.position - self.__mover.position ).length()
		print( "distance_from_obstacle:", distance )
		return distance

	def track_target_coreBody_angle( self, task ):
		if self.__mover.currentTarget is None:
			return task.cont
		h_diff, new_hpr = self.__getRelativeHpr( self.__mover.coreBodyPath, self.__mover.currentTarget.position, tracking_speed = 50 )
		self.__mover.coreBodyPath.setHpr( new_hpr )
		if abs( h_diff ) <= 50:
			self.__mover.aligned = True
		else:
			self.__mover.aligned = False
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
		return self.__detector.detectObstacle( target )

	def target_detection( self, task ):
		if self.__tempTarget is not None:
			self.__mover.bpTarget = self.__tempTarget
			self.__tempTarget = None
			return task.done
		detection = self.__detector.detectAlternativePosition( self.__getCurrentTarget() )
		if detection:
			self.__tempTarget = CustomTarget( detection.position )
		return task.cont

	def __getCurrentTarget( self ):
		return self.__mover.currentTarget

	def generateAndCheckNewCurve( self, positions, obstacle ):
		curve = self._curveGenerator.generateNewCurve( positions )
		return not self._curveGenerator.checkCurveObstacleContact( curve, obstacle )

	def getCurvePoints( self ):
		return self._curveGenerator.getCurveTargets()

	def terminateCurve( self ):
		self._curveGenerator.terminateCurve()

