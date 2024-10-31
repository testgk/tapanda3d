from direct.interval.LerpInterval import LerpHprInterval
from direct.task import Task
from panda3d.core import LVector3, Vec3

from phyisics import globalClock


class MovementManager:
    def __init__( self, entity ):
        self.__entity = entity

    def update( self ):
        pass

    def rotate( self, degrees ):
        rotation_duration = 6
        current_hpr = Vec3( self.__entity.coreBody.getHpr() )
        rotation_interval = LerpHprInterval( self.__entity.coreBody, rotation_duration, (  current_hpr.x +  degrees, 0, 0) )
        rotation_interval.start()

    def velocity( self, velocity, angle  ):
        # Assuming 'velocity' is a float or int representing the speed
        direction = LVector3( Vec3( angle, 0, 0 ) )  # Desired direction along the X-axis

        # Multiply direction by speed
        velocity_vector = direction * float( velocity )

        # Apply to rigid body
        self.__entity.coreRigidBody.setLinearVelocity( velocity_vector )

    #def track_target_velocity( self, target_velocity ):

    def track_target_angle(self, angle ):
        tracking_speed = 10
        current_hpr = Vec3( self.__entity.coreBody.getHpr() )
        target_angle = Vec3( angle, 0, 0 )

        # Calculate the shortest angle difference for each component (H, P, R)
        h_diff = target_angle.x - current_hpr.x
        p_diff = target_angle.y - current_hpr.y
        r_diff = target_angle.z - current_hpr.z
        print( f"Current H: {current_hpr.x}, Target H: {target_angle.x}, h_diff: {h_diff}" )
        # Clamp the rotation speed to the tracking speed per frame
        h_adjust = max( - tracking_speed * globalClock.getDt(), min( h_diff, tracking_speed * globalClock.getDt() ) )
        p_adjust = max( - tracking_speed * globalClock.getDt(), min( p_diff, tracking_speed * globalClock.getDt() ) )
        r_adjust = max( - tracking_speed * globalClock.getDt(), min( r_diff, tracking_speed * globalClock.getDt() ) )

        print( f"h_adjust: {h_adjust}, p_adjust: {p_adjust}, r_adjust: {r_adjust}" )
        if abs( h_diff ) < 0.1:
            return True
        # Apply the adjustments to the current HPR
        new_hpr = current_hpr + Vec3( h_adjust, p_adjust, r_adjust )

        self.__entity.coreBody.setHpr( new_hpr )
        return False