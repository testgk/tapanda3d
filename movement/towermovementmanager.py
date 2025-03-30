import math
from typing import TYPE_CHECKING

from panda3d.core import Vec3
from phyisics import globalClock


class TowerMovementManager:
	def __init__( self, entity ):
		self.__tower = entity

	def track_target_coreBody_angle( self, task ):
		if self.__tower.currentTarget is None:
			return task.cont
		h_diff, new_hpr = self._getRelativeHpr( self.__tower.coreBodyPath, self.__tower.currentTarget.position, tracking_speed = 50 )
		self.__tower.coreBodyPath.setHpr( new_hpr )
		if abs( h_diff ) <= 50:
			self.__tower.aligned = True
		else:
			self.__tower.aligned = False
		return task.cont


	def _getRelativeHpr( self, bodyPart, target_position, tracking_speed = 100 ):
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