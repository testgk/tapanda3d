import math
from direct.task import Task
from panda3d.core import Point3, Vec4

from picker import Picker
from cameracontroller import CameraController



class TerrainCamera:
    CLOSE_PROXIMITY = 400

    def __init__(self, camera, mouseWatcherNode, camNode, render, terrainCenter: Point3 ):
        self.__last_custom_collision_polygon = None
        self.camera_controller = None
        self.camera = camera
        self.__render = render
        self.mouseWatcherNode = mouseWatcherNode
        self.camNode = camNode
        self.__terrainCenter = terrainCenter
        self.__center = terrainCenter
        self.__cameraHeight = None
        self.__cameraRadius = None
        self.__cameraAngle = None
        self.__terrainPicker = Picker( self.camera )
        self.camera.lookAt( self.__center )
        self.setCamera()

    def setCamera( self ):
        self.__cameraAngle = 0  # Initial camera angle
        self.__cameraRadius = 1200  # Distance from the __center of the terrain
        self.__cameraHeight = 400  # Height of the camera

    def rotateCamera( self, direction = 1 ):
        self.__cameraAngle += math.radians( direction * 10 )  # Rotate by 10 degrees per click
        self.__updateCameraPosition()

    def zoomCamera( self, value ):
        self.__cameraHeight += value

    @property
    def center( self ):
        return self.__center

    def hoverAbove( self ):
        self.__cameraAngle = 0  # Initial camera angle
        self.__cameraRadius = 0  # Distance from the __center of the terrain
        self.__cameraHeight = 1200  # Height of the camera
        self.__updateCameraPositionAndCenter()

    def hoverDistance( self ):
        self.__cameraAngle = 0  # Initial camera angle
        self.__cameraRadius = 1200  # Distance from the __center of the terrain
        self.__cameraHeight = 400  # Height of the camera
        self.__updateCameraPosition()

    def __updateCameraPositionAndCenter( self ):
        self.__center = self.__terrainCenter
        print(f" center: { self.__terrainCenter }")

    def __updateCameraPosition( self, center = None ):
        self.camera_controller = CameraController( self.camera,
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

    def isCenterdOnPoly( self ):
        if self.__last_custom_collision_polygon is None:
            return True
        distance = ( self.__last_custom_collision_polygon.surfacePosition - self.surfaceCenter ).length()
        print(  f'position { self.__last_custom_collision_polygon.surfacePosition }, center: { self.surfaceCenter }, distance: { distance }' )
        return distance < 20

    def getNewEntry( self ):
        if self.mouseWatcherNode.hasMouse():
            mousePosition = self.mouseWatcherNode.getMouse()
            self.__terrainPicker.pickerRay.setFromLens( self.camNode, mousePosition.getX(), mousePosition.getY() )
            self.__terrainPicker.picker.traverse( self.__render )
            numEntries = self.__terrainPicker.pickerQueue.getNumEntries()
            if numEntries > 0:
                self.__terrainPicker.pickerQueue.sortEntries()
                entry = self.__terrainPicker.pickerQueue.getEntry( 0 )
                return entry

    def on_map_click( self ):
        entry = self.getNewEntry()
        picked_obj = entry.getIntoNodePath()
        point = entry.getSurfacePoint( self.__render )
        print( f"Clicked node: { picked_obj }" )
        custom_collision_polygon = picked_obj.node().getPythonTag( 'custom_collision_polygon' )
        if custom_collision_polygon:
            if self.__last_custom_collision_polygon:
                self.__last_custom_collision_polygon.hideNeighbors()
            print( f"CustomCollisionPolygon instance: { custom_collision_polygon }" )
            print( f"Parent node: { custom_collision_polygon.name }" )
            custom_collision_polygon.hideNeighbors()
            custom_collision_polygon.showNeighbors( custom_collision_polygon.row, custom_collision_polygon.col,4 )
            custom_collision_polygon.showDebugNode()
            custom_collision_polygon.setColorDebugNode( Vec4( 0, 0, 0, 0.5 ) )
            self.__last_custom_collision_polygon = custom_collision_polygon

    def on_map_hover( self ):
        entry = self.getNewEntry()
        if entry:
            point = entry.getSurfacePoint( self.__render )
            self.__center = point
