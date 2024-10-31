from direct.interval.LerpInterval import LerpHprInterval
from direct.task import Task
from panda3d.core import Vec3

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

    def velocity( self, velocity ):
        self.__entity.coreRigidBody.set_linear_velocity( velocity )

    def track_target_velocity( self, target_velocity ):


    def track_target_angle(self, angle ):
        # Get the model's current HPR
        tracking_speed = 10
        current_hpr = Vec3( self.__entity.coreBody.getHpr() )
        target_angle = Vec3( angle, 0, 0 )
        h_diff = target_angle.x - current_hpr.x
        #print( f"Current H: {current_hpr.x}, Target H: {target_angle.x}, h_diff: {h_diff}" )
        h_adjust = max( - tracking_speed * globalClock.getDt(), min(h_diff, tracking_speed * globalClock.getDt() ) )
        #print( f"h_adjust: {h_adjust}, p_adjust: {p_adjust}, r_adjust: {r_adjust}" )
        #if abs( h_diff ) < 0.1:
        #    return True
        new_hpr = current_hpr + Vec3( h_adjust, 0, 0 )
        self.__entity.coreBody.setHpr( new_hpr )
        return False
