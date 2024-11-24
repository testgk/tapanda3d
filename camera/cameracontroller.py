import math
from panda3d.core import Camera, Vec3
from direct.interval.LerpInterval import LerpPosInterval, LerpHprInterval


class CameraController:
    def __init__( self, camera: Camera, center, cameraRadius = 10, cameraHeight = 10, cameraAngle = 0,
                  transitionTime = 1 ):
        self.__reachedPosition = False
        self.camera = camera
        self.__center = center
        self.__cameraRadius = cameraRadius
        self.__cameraHeight = cameraHeight
        self.__cameraAngle = cameraAngle
        self.__transitionTime = transitionTime

    def updateCameraPosition( self ):
        x = self.__center.getX() + ( self.__cameraRadius ) * math.sin( self.__cameraAngle )
        y = self.__center.getY() + ( self.__cameraRadius ) * math.cos( self.__cameraAngle )
        z = self.__cameraHeight
        self.targetPos = Vec3( x, y, z )
        self.camera.setPos( self.targetPos  )
        self.camera.lookAt( self.__center )
        self.targetHpr = self.camera.getHpr()
        self.camera.setHpr( self.targetHpr )
        posInterval = LerpPosInterval( self.camera, self.__transitionTime, self.targetPos  )
        hprInterval = LerpHprInterval( self.camera, self.__transitionTime, self.targetHpr )

        # Start the intervals
        posInterval.start()
        hprInterval.start()

    def updateParameters( self, center, cameraRadius, cameraHeight, cameraAngle ):
        self.__center = center
        self.__cameraRadius = cameraRadius
        self.__cameraHeight = cameraHeight
        self.__cameraAngle = cameraAngle