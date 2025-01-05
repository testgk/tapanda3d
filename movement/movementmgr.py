import math
import queue
import random
from collections import deque

from panda3d.core import LineSegs, NodePath, Vec3

from enums.directions import Direction
from phyisics import globalClock
from typing import TYPE_CHECKING

from selectionmodes import SelectionModes

if TYPE_CHECKING:
    from entities.full.movers.mover import Mover

class MovementManager:
    def __init__( self, entity, world ):
        self.__tempTargets = None
        self.__mover: Mover = entity
        self.__aligned = False
        self.__world = world
        self.__ray1 = None
        self.__ray2 = None
        self.__ray3 = None

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
        if not self.__aligned:
            return task.cont
        obstacle = self.__checkForObstacles()
        try:
            if obstacle is None:
                if self.__mover.obstacle is not None:
                    self.__mover.obstacle.clearSelection()
                    self.__mover.obstacle = obstacle
                return task.cont
            return task.done
        finally:
            self.__mover.obstacle = obstacle

    def monitor_handle_obstacles( self, task ):
        obstacle = self.__checkForObstacles()
        try:
            if obstacle is None:
                if self.__mover.obstacle is not None:
                    self.__mover.obstacle.clearSelection()
                    self.__mover.obstacle = obstacle
                    return task.done
            return task.cont
        finally:
            self.__mover.obstacle = obstacle

    def __checkForObstacles( self ):
        target = self.__mover.currentTarget.position
        position = self.__mover.position
        direction = Vec3( target.x -  self.__mover.edgePos().x, target.y -  self.__mover.edgePos().y, 10 )
        # Calculate the angle in radians using atan2
        angle_radians = math.atan2( self.__mover.width,  self.__mover.height )
        # Now create the direction vector based on the angle
        direction = Vec3( math.cos( angle_radians ), math.sin( angle_radians ), 10 )
        if self.__ray1:
            self.__ray1.remove_node()
        if self.__ray2:
            self.__ray2.remove_node()
        if self.__ray3:
            self.__ray3.remove_node()
        #self.__ray1 = self.visualize_ray( start = self.__mover.position + self.__mover.offset, end = target + self.__mover.offset + direction * 10  )
        #self.__ray2 = self.visualize_ray( start = self.__mover.position - self.__mover.offset, end = target - self.__mover.offset + direction * 10 )
        self.__ray3 = self.visualize_ray( start = self.__mover.edgePos() , end = self.__mover.edgePos() + direction * 10 )
        #result1 = self.__world.rayTestAll( positionWithOffsetLeft(), target + direction * 10 )
        #result2 = self.__world.rayTestAll( positionWithOffsetRight(), target + direction * 10 )
        result3 = self.__world.rayTestAll(  self.__mover.edgePos(), target + direction * 10 )
        for result in [ result3 ]:
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
                        obstacle.handleSelection()
                        return obstacle
        return None

    def alternative_target( self, task ):
        if self.__mover.currentTarget is None:
            return task.done
        if not self.__mover.hasObstacles():
            for target in self.__mover.selectTargets:
                target.clearSelection()
            #for target in self.__tempTargets:
            #self.__tempTargets.clearSelection()
            #self.__mover.selectTargets.clear()
            self.__mover.selectTargets.appendleft( self.__mover.currentTarget )
            self.__mover.currentTarget.handleSelection( SelectionModes.P2P )
            #print( f'temp targets: { len(self.__tempTargets)} ')
            #if self.__tempTargets is not None:
            #    self.__mover.selectTargets.appendleft( self.__tempTargets )
            #self.__tempTargets = None
            #self.__mover.displayTargets()
            return task.done

        #self.__tempTargets = self.__mover.currentTarget
        print( f'adding : { self.__mover.currentTarget } ' )
        self.__mover.currentTarget.clearSelection()
        self.__mover.currentTarget = self.__mover.currentTarget.randomNeighbor()
        self.__mover.currentTarget.handleSelection( SelectionModes.CHECK )
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

    def visualize_ray( self, start, end, color = (1, 0, 0, 1), thickness = 2.0 ):
        line = LineSegs()
        line.set_thickness( thickness )
        line.set_color( *color )  # RGBA
        line.move_to( start )
        line.draw_to( end )
        line_node = NodePath( line.create() )
        line_node.reparent_to( self.__mover.render )
        return line_node

    def __getFrontEdges( self ):
        x = self.__mover.collisionBox.get_tight_bounds()
        min_point, max_point = self.__mover.collisionBox.get_tight_bounds()
        bottom_front_left = Vec3( min_point.x, min_point.y, min_point.z )
        bottom_front_right = Vec3( max_point.x, min_point.y, min_point.z )
        return ( bottom_front_left, bottom_front_right )

    def __getOffsets( self ):
        position = self.__mover.position
        pointA = position + self.__mover.offset
        pointB = position - self.__mover.offset
        distance = ( pointB - pointA ).length()
        if distance >= self.__mover.width:
            return  self.__mover.offset, self.__mover.offset


    def get_edge_positions( width, heading ):
        # Calculate half-width
        half_width = se / 2.0

        # Convert heading to radians
        heading_rad = math.radians( heading )

        # Calculate offsets
        left_offset = Vec3( -half_width * math.cos( heading_rad ), -half_width * math.sin( heading_rad ), 0 )
        right_offset = Vec3( half_width * math.cos( heading_rad ), half_width * math.sin( heading_rad ), 0 )
        return left_offset, right_offset


