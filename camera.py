import math
from direct.task import Task
from panda3d.core import Point3
from cameracontroller import CameraController



class TerrainCamera:
    CLOSE_PROXIMITY = 400

    def __init__(self, camera, terrainCenter: Point3 ):
        self.target = None
        self.__last_custom_collision_polygon = None
        self.__camera = camera
        self.__terrainCenter = terrainCenter
        self.__center = terrainCenter
        self.__cameraHeight = None
        self.__cameraRadius = None
        self.__cameraAngle = None
        self.__camera.lookAt( self.__center )
        self.setCamera()
        self.camera_controller = CameraController( self.__camera,
                                                   self.__center,
                                                   cameraRadius = self.__cameraRadius,
                                                   cameraHeight = self.__cameraHeight,
                                                   cameraAngle = self.__cameraAngle )

    def setCamera( self ):
        self.__cameraAngle = 0  # Initial __camera angle
        self.__cameraRadius = 1200  # Distance from the __center of the terrain
        self.__cameraHeight = 400  # Height of the __camera

    def rotateCamera( self, direction = 1 ):
        self.__cameraAngle += math.radians( direction * 10 )  # Rotate by 10 degrees per click
        self.__updateCameraPosition()

    def zoomCamera( self, value ):
        self.__cameraHeight += value

    def zoomCenter( self, value ):
        self.__cameraRadius += ( value * 10 )
        self.__cameraHeight += value

    @property
    def center( self ):
        return self.__center

    def hoverAbove( self ):
        self.__cameraAngle = 0  # Initial __camera angle
        self.__cameraRadius = 0  # Distance from the __center of the terrain
        self.__cameraHeight = 1200  # Height of the __camera
        self.__updateCameraPositionAndCenter()

    def hoverDistance( self ):
        self.__cameraAngle = 0  # Initial __camera angle
        self.__cameraRadius = 1200  # Distance from the __center of the terrain
        self.__cameraHeight = 400  # Height of the __camera
        self.__updateCameraPosition()

    def __updateCameraPositionAndCenter( self ):
        self.__center = self.__terrainCenter
        print( f" center: { self.__terrainCenter }")

    def __updateCameraPosition( self ):
        self.camera_controller.updateParameters(
            self.__center,
            cameraRadius = self.__cameraRadius,
            cameraHeight = self.__cameraHeight,
            cameraAngle = self.__cameraAngle )
        self.camera_controller.updateCameraPosition()

    def updateCameraTask( self, task ):
        self.__updateCameraPosition()
        return Task.cont  # Continue the task

    @property
    def surfaceCenter( self ):
        return Point3( self.__center[ 0 ], self.__center[ 1 ], 0 )

    def setCenter( self, point ) :
        self.__center = point
