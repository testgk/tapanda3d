import math

from direct.interval.LerpInterval import LerpHprInterval
from direct.task import Task
from panda3d.core import LVector3, Vec3

from phyisics import globalClock


class MovementManager:
    def __init__( self, entity ):
        self.__entity = entity
        self.__adjusted = False

    def update( self ):
        pass

    def rotate( self, degrees ):
        rotation_duration = 6
        current_hpr = Vec3( self.__entity.coreBody.getHpr() )
        rotation_interval = LerpHprInterval( self.__entity.coreBody, rotation_duration, (  current_hpr.x +  degrees, 0, 0) )
        rotation_interval.start()

    def velocity( self, velocity  ):
        if not self.__adjusted:
            return
        rotation_quat = self.__entity.coreBody.getQuat()
        local_forward = LVector3( 1, 0, 0 )
        forward_direction = rotation_quat.xform( local_forward )
        velocity_vector = forward_direction.normalized() * velocity
        print( f"Apply velocity: {velocity_vector }" )
        self.__entity.coreRigidBody.setLinearVelocity( velocity_vector )

    #def track_target_velocity( self, target_velocity ):

    def track_target_angle(self, angle ):
        tracking_speed = 30
        current_hpr = Vec3( self.__entity.coreBody.getHpr() )
        target_angle = Vec3( angle, 0, 0 )
        h_diff = target_angle.x - current_hpr.x
        print( f"Current H: { current_hpr.x }, Target H: { target_angle.x }, h_diff: { h_diff }" )
        h_adjust = max( - tracking_speed * globalClock.getDt(), min( h_diff, tracking_speed * globalClock.getDt() ) )
        new_hpr = current_hpr + Vec3( h_adjust,  0,  0 )
        self.__entity.coreBody.setHpr( new_hpr )
        print( f"h_adjust: { h_adjust }, h_diff: { h_diff }" )
        if abs( h_diff ) ==0:
            self.__adjusted = True
            return True
        self.__adjusted = False
        return False

    def follow_a_path( self, point_b, speed = 20 ):
        current_pos = self.__entity.coreBody.getPos()

        # Calculate direction to the target point (point B)
        direction = (point_b - current_pos).normalized()

        # Set velocity towards the target point
        velocity = direction * speed
        self.__entity.coreRigidBody.setLinearVelocity( velocity )

        # Rotate the model to face the direction of movement
        angle = math.degrees( math.atan2( direction.y, direction.x ) )
        self.__entity.coreBody.setH( angle )