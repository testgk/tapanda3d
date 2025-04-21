
import math
from panda3d.core import Vec3

from entities.locatorMode import LocatorModes
from movement.curve import CurveGenerator
from movement.obstacledetector import ObstacleDetector
from movement.towermovementmanager import TowerMovementManager
from phyisics import globalClock
from typing import TYPE_CHECKING

from target import CustomTarget

if TYPE_CHECKING:
	from entities.full.movers.mover import Mover


class MovementManager( TowerMovementManager ):
	def __init__( self, entity, world, render ):
		super().__init__( entity, world, render )
		self._curveGenerator = CurveGenerator( world, render )
		self.__tempTarget = None
		self.__mover: Mover = entity

	def set_velocity_toward_point_with_stop( self, task ):
		if not self.__mover.currentTarget:
			return task.cont
		if not self.__mover.aligned:
			return task.cont
		speed = self.__mover.speed
		target_pos = self.__mover.currentTarget.position
		current_pos = self.__mover.position
		direction = Vec3( target_pos.x - current_pos.x, target_pos.y - current_pos.y, 0 )
		distance = direction.length()
		if distance < 20:
			if self.__mover.stopDistance:
				self.stopMovement()
			self.__mover.clearCurrentTarget()
			return task.cont
		direction.normalize()
		velocity = direction * speed
		self.__mover.coreRigidBody.set_linear_velocity( velocity )
		return task.cont

	def stopMovement( self ):
		print( f"{ self.__mover.name } is stopping" )
		self.__mover.coreRigidBody.set_linear_velocity( Vec3( 0, 0, 0 ) )
		self.__mover.coreRigidBody.set_angular_velocity( Vec3( 0, 0, 0 ) )

	def set_velocity_backwards_direction( self, task ):
		if not self.__mover.closeToObstacle():
			return task.done
		direction = Vec3( self.__mover.obstacle.position - self.__mover.position )
		direction.normalize()
		self.__mover.coreRigidBody.set_linear_velocity( direction * self.__mover.speed )
		return task.cont

	def distanceFromObstacle( self ):
		distance = ( self.__mover.obstacle.position - self.__mover.position ).length()
		print( "distance_from_obstacle:", distance )
		return distance

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
		#if not self.__entity.aligned:
		#	return task.cont
		if self.__mover.locatorMode == LocatorModes.NONE:
			return task.done
		if self.__mover.obstacle is not None:
			return task.cont
		#if self.__entity.currentTarget is None:
		#	return task.again
		obstacle = self.__checkForObstacles( self._getCurrentTarget() )
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
		return self._detector.detectObstacle( target )

	def target_detection( self, task ):
		if self.__tempTarget is not None:
			self.__mover.bypassTarget = self.__tempTarget
			self.__tempTarget = None
			return task.done
		detection = self._detector.detectAlternativePosition( self._getCurrentTarget() )
		if detection:
			self.__tempTarget = CustomTarget( detection.position )
		return task.cont

	def maintain_turret_angle( self, task ):
		return super().maintain_turret_angle( task )

	def generateAndCheckNewCurve( self, positions, obstacle ):
		curve = self._curveGenerator.generateNewCurve( positions )
		return self._curveGenerator.checkCurveObstacleContact( curve, obstacle )

	def getCurvePoints( self ):
		return self._curveGenerator.getCurveTargets()

	def terminateCurve( self ):
		self._curveGenerator.terminateCurve()

