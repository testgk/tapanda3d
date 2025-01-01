import math
import queue
import random
from collections import deque

from panda3d.core import Vec3

from enums.directions import Direction
from phyisics import globalClock
from typing import TYPE_CHECKING

from selectionmodes import SelectionModes

if TYPE_CHECKING:
    from entities.full.movers.mover import Mover

class MovementManager:
    def __init__( self, entity, world ):
        self.__tempTargets = deque()
        self.__mover: Mover = entity
        self.__aligned = False
        self.__world = world

    def set_velocity_toward_point_with_stop( self, target_pos, task ):
        speed = self.__mover.regularSpeed
        stop_threshold = 20
        if not self.__aligned:
            return task.cont
        if self.__mover.hasObstacles():
            return task.done
        current_pos = self.__mover.position
        direction = Vec3( target_pos.x - current_pos.x, target_pos.y - current_pos.y, 0 )
        distance = direction.length()
        if distance < stop_threshold:
            self.__mover.coreRigidBody.set_linear_velocity( Vec3( 0, 0, 0 ) )
            return task.done
        direction.normalize()
        velocity = direction * speed
        self.__mover.coreRigidBody.set_linear_velocity( velocity )
        return task.cont

    def track_target_angle( self, task ):
        if self.__mover.currentTarget is None:
            return task.cont
        h_diff, new_hpr = self.__getRelativeHpr( self.__mover.coreBodyPath, self.__mover.currentTarget.position,  tracking_speed = 50 )
        self.__mover.coreBodyPath.setHpr( new_hpr )
        if abs( h_diff ) <= 5:  # Small threshold for floating-point precision
            self.__aligned = True
            #print( f'{self.__mover.name} is aligned' )
        else:
            self.__aligned = False
            #print( f'{ self.__mover.name } is not aligned' )
        return task.cont

    def __getRelativeHpr( self, bodyPart,  target_position, tracking_speed = 100 ):
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

    def maintain_turret_angle( self, target, task ):
        if self.__mover.finishedMovement():
            print( f'{ self.__mover.name } finished angle tracking' )
            return task.done
        h_diff, new_hpr = self.__getRelativeHpr( self.__mover.turretBase().rigidBodyPath, target, tracking_speed = 25 )
        self.__mover.turretBase().rigidBodyPath.setHpr( new_hpr )
        return task.cont

    def monitor_obstacles( self, task ):
        if self.__mover.currentTarget is None:
            return task.done
        self.__mover.obstacle = self.__checkFoeObstacles()
        if self.__mover.obstacle is None:
            return task.cont
        return task.done

    def monitor_obstacles_1( self, task ):
        self.__mover.obstacle = self.__checkFoeObstacles()
        if self.__mover.obstacle is None:
                return task.done
        return task.cont

    def __checkFoeObstacles( self ):
        target = self.__mover.currentTarget.position
        direction = Vec3( target.x - self.__mover.position.x, target.y - self.__mover.position.y, 10 )
        result = self.__world.rayTestAll( self.__mover.position, target + direction * 5 )
        if result.hasHits():
            for hit in result.getHits():
                hit_node = hit.getNode()
                if self.__mover.selfHit( hit_node ):
                    continue
                try:
                    obstacle = hit_node.getPythonTag( 'raytest_target' )
                except AttributeError:
                    continue
                if obstacle is None:
                    continue
                elif obstacle.isObstacle:
                    return obstacle
        return None

    def alternative_target( self, task ):
        if self.__mover.currentTarget is None:
            return task.done
        if not self.__mover.hasObstacles():
            for target in self.__mover.selectTargets:
                target.clearSelection()
            self.__mover.selectTargets.clear()
            self.__mover.selectTargets.appendleft( self.__mover.currentTarget )
            print( f'temp targets: { len(self.__tempTargets)} ')
            if any( self.__tempTargets ):
                self.__mover.selectTargets.appendleft( self.__tempTargets.pop() )
            self.__tempTargets.clear()
            self.__mover.displayTargets()
            return task.done

        self.__tempTargets.append( self.__mover.currentTarget )
        print( f'adding : { self.__mover.currentTarget } ' )
        newTarget = self.__mover.currentTarget.randomNeighbor()
        self.__mover.currentTarget = newTarget
        self.__mover.currentTarget.handleSelection( SelectionModes.P2P )
        print( f'current target: { self.__mover.currentTarget }' )
        self.__aligned = False
        return task.cont

    def maintain_terrain_boundaries( self, terrainSize, task ):
        current_pos = self.__mover.coreBodyPath.get_pos()
        if current_pos.x <= 10:
            self.__mover.coreBodyPath.setPos( Vec3( 11, current_pos.y, current_pos.z ) )
            return task.cont
        elif current_pos.x >= terrainSize - 10:
            self.__mover.coreBodyPath.setPos( Vec3( terrainSize - 9, current_pos.y, current_pos.z ) )
        if current_pos.y <= 10:
            self.__mover.coreBodyPath.setPos( Vec3( current_pos.x, 11 , current_pos.z ) )
            return task.cont
        elif current_pos.y >= terrainSize - 10:
            self.__mover.coreBodyPath.setPos( Vec3( current_pos.x, terrainSize - 9, current_pos.z ) )
        return task.cont
