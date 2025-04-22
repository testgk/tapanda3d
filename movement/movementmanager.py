from typing import TYPE_CHECKING
from panda3d.core import Vec3, Mat3

from target import CustomTarget
from movement.curve import CurveGenerator
from entities.locatorMode import LocatorModes
from movement.stationarymovementmanager import StationaryMovementManager




if TYPE_CHECKING:
	from entities.full.movers.mover import Mover


class MovementManager(StationaryMovementManager):
	TARGET_DISTANCE_THRESHOLD = 20
	ZERO_VELOCITY_VEC = Vec3( 0, 0, 0 )

	def __init__( self, entity: 'Mover', world, render ):
		super().__init__( entity, world, render )
		self.__curveGenerator = CurveGenerator(world, render)
		self.__alternativeTarget = None
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
		if distance < self.TARGET_DISTANCE_THRESHOLD:
			if self.__mover.stopAtDistance:
				self.stopMovement()
			self.__mover.clearCurrentTarget()
			return task.cont
		direction.normalize()
		velocity = direction * speed
		self.__mover.coreRigidBody.set_linear_velocity( velocity )
		return task.cont

	def stopMovement( self ):
		print( f"{ self.__mover.name } is stopping" )
		self.__mover.coreRigidBody.set_linear_velocity( self.ZERO_VELOCITY_VEC )
		self.__mover.coreRigidBody.set_angular_velocity( self.ZERO_VELOCITY_VEC )

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

	def maintain_terrain_boundaries( self, terrainSize: int, task ):
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
		if self.__mover.locatorMode == LocatorModes.NONE:
			return task.done
		if self.__mover.obstacle is not None:
			return task.cont
		obstacle = self.obstacleDetector.detectObstacle(self._getCurrentTarget())
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
			return task.cont

	def alternateTargetDetection(self, task):
		if self.__alternativeTarget is not None:
			self.__mover.bypassTarget = self.__alternativeTarget
			self.__alternativeTarget = None
			return task.done
		self.__findAlternativeTarget()
		return task.cont

	def __findAlternativeTarget(self) -> None:
		vec = self.__mover.position - self.__mover.obstacle.position
		rotation_matrix = Mat3.rotateMatNormaxis( 90, Vec3( 0, 0, 1) )
		rotated_vec = rotation_matrix.xform( vec )
		c = self.__mover.obstacle.position + rotated_vec
		self.__alternativeTarget = CustomTarget( position = c )

	def maintain_turret_angle( self, task ):
		return super().maintain_turret_angle( task )

	def generateAndCheckNewCurve( self, positions, obstacle ):
		curve = self.__curveGenerator.generateNewCurve( positions )
		return self.__curveGenerator.checkCurveObstacleContact( curve, obstacle )

	def getCurvePoints( self ):
		return self.__curveGenerator.getCurveTargets()

	def terminateCurve( self ):
		self.__curveGenerator.terminateCurve()

