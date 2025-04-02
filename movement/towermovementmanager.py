import math
from typing import TYPE_CHECKING

from panda3d.core import Vec3
from phyisics import globalClock

if TYPE_CHECKING:
	from entities.full.movers.mover import Mover
	from entities.full.towers.towers import Tower


class TowerMovementManager:

	def __init__( self, entity ):
		self.__tower: Tower | Mover = entity

	def track_target_coreBody_angle( self, task ):
		task.delayTime = 0.5
		if self._getCurrentTarget() is None:
			return task.again
		h_diff, new_hpr = self._getRelativeHpr( self.__tower.coreBodyPath,
												self.__tower.currentTarget.position,
												tracking_speed = 50 )
		self.__tower.coreBodyPath.setHpr( new_hpr )
		if abs( h_diff ) <= 5:
			self.__tower.aligned = True
			return task.again
		else:
			self.__tower.aligned = False
		return task.cont

	def _getRelativeHpr( self, bodyPart, target_position, tracking_speed = 100 ):
		current_pos = bodyPart.getPos()
		current_hpr = Vec3( bodyPart.getHpr() )
		direction_vector = target_position - current_pos
		target_heading = math.degrees( math.atan2( direction_vector.y, direction_vector.x ) )
		h_diff = (Vec3( target_heading, 0, 0 ).x - current_hpr.x + 180) % 360 - 180
		h_adjust = max( -tracking_speed * globalClock.getDt(), min( h_diff, tracking_speed * globalClock.getDt() ) )
		return h_diff, current_hpr + Vec3( h_adjust, 0, 0 )

	def maintain_turret_angle( self, task ):
		if self._getCurrentTarget() is None:
			return task.cont
		h_diff, new_hpr = self._getRelativeHpr( self.__tower.turretBase().rigidBodyPath,
		                                        self._getCurrentTarget().position, tracking_speed = 25 )
		self.__tower.turretBase().rigidBodyPath.setHpr( new_hpr )
		return task.cont

	def isAlignedToTarget( self, task ):
		if self._getCurrentTarget() is None:
			return task.cont
		if self.__tower.aligned:
			if self._getCurrentTarget().isTerrain:
				self.__tower.clearCurrentTarget()
		return task.cont

	def _getCurrentTarget( self ):
		return self.__tower.currentTarget
