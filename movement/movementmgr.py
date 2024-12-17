import math
from time import perf_counter
from panda3d.core import LVector3, Vec3

from phyisics import globalClock
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.full.movers.mover import Mover

class MovementManager:
    def __init__( self, entity ):
        self.__entity: Mover = entity
        self.__aligned = False

    def set_velocity_toward_point_with_stop( self, target_pos, task ):
        speed = 100
        stop_threshold = 20
        if not self.__aligned:
            return task.cont
        current_pos = self.__entity.coreBodyPath.get_pos()
        direction = Vec3( target_pos.x - current_pos.x, target_pos.y - current_pos.y, 0 )
        distance = direction.length()
        if distance < stop_threshold:
            self.__entity.coreRigidBody.set_linear_velocity( Vec3( 0, 0, 0 ) )
            return task.done
        direction.normalize()
        velocity = direction * speed
        self.__entity.coreRigidBody.set_linear_velocity( velocity )
        return task.cont

    def track_target_angle( self, target_position, task ):
        if self.__entity.finishedMovement():
            print( f'{ self.__entity.name } finished angle tracking' )
            return task.done
        h_diff, new_hpr = self.__getRelativeHpr( self.__entity.coreBodyPath, target_position )
        self.__entity.coreBodyPath.setHpr( new_hpr )
        if abs( h_diff ) <= 5:  # Small threshold for floating-point precision
            self.__aligned = True
        else:
            self.__aligned = False
            print( f'{ self.__entity.name } is not aligned' )
        return task.cont

    def __getRelativeHpr( self, bodyPart, target_position, tracking_speed = 100 ):
        current_pos = bodyPart.getPos()
        current_hpr = Vec3( bodyPart.getHpr() )
        direction_vector = target_position - current_pos
        target_heading = math.degrees( math.atan2( direction_vector.y, direction_vector.x ) )  # atan2(y, x)
        target_hpr = Vec3( target_heading, 0, 0 )
        h_diff = target_hpr.x - current_hpr.x
        h_diff = ( h_diff + 180 ) % 360 - 180
        h_adjust = max( -tracking_speed * globalClock.getDt(), min( h_diff, tracking_speed * globalClock.getDt() ) )
        new_hpr = current_hpr + Vec3( h_adjust, 0, 0 )
        return h_diff, new_hpr

    def maintain_turret_angle( self, target, task ):
        if self.__entity.finishedMovement():
            print( f'{ self.__entity.name } finished angle tracking' )
            return task.done
        h_diff, new_hpr = self.__getRelativeHpr( self.__entity.turretBase().rigidBodyPath, target, tracking_speed = 25 )
        self.__entity.turretBase().rigidBodyPath.setHpr( new_hpr )
        return task.cont