from panda3d.core import Camera, Vec3
from direct.interval.LerpInterval import LerpPosInterval, LerpHprInterval
from direct.interval.IntervalGlobal import Sequence
import math


class CameraController:
    def __init__( self, camera: Camera, center, cameraRadius = 10, cameraHeight = 10, cameraAngle = 0,
                  transitionTime = 1 ):
        self.camera = camera
        self.__center = center
        self.__cameraRadius = cameraRadius
        self.__cameraHeight = cameraHeight
        self.__cameraAngle = cameraAngle
        self.__transitionTime = transitionTime

    def updateCameraPosition( self ):
        # Calculate new camera position on a circular path around the terrain __center
        x = self.__center.getX() + ( self.__cameraRadius ) * math.sin( self.__cameraAngle )
        y = self.__center.getY() + ( self.__cameraRadius ) * math.cos( self.__cameraAngle )
        z = self.__cameraHeight

        # Target position
        targetPos = Vec3( x, y, z )
        #print( f'targetPos { targetPos }' )

        # Temporarily set camera position to calculate the correct HPR
        self.camera.setPos( targetPos )
        self.camera.lookAt( self.__center )

        # Get the target HPR (heading, pitch, roll)
        targetHpr = self.camera.getHpr()

        # Reset the camera to its original orientation (optional, depending on if you want to interpolate from current position)
        self.camera.setHpr(targetHpr)

        # Create interpolation intervals
        posInterval = LerpPosInterval( self.camera, self.__transitionTime, targetPos )
        hprInterval = LerpHprInterval( self.camera, self.__transitionTime, targetHpr )

        # Start the intervals
        posInterval.start()
        hprInterval.start()