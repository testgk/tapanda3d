from lights import Lights
from camera import TerrainCamera
from camerabuttons import CameraButtons
from terraincolision import TerrainCollision
from direct.showbase.ShowBase import ShowBase
from maps.terrainprovider import TerrainProvider
from direct.task import Task

class MyApp( ShowBase ):
    def __init__( self ):
        ShowBase.__init__( self )
        self.camera_centered = False
        terrainProvider = TerrainProvider( self.loader )
        self.terrainInfo = terrainProvider.create_terrain( "heightmap1" )
        self.terrain = self.terrainInfo.terrain

        self.terrain.getRoot().reparentTo( self.render )
        self.terrain.setFocalPoint( self.camera )
        self.disableMouse()
        self.terrainCamera = TerrainCamera( self.camera,
                                            self.mouseWatcherNode,
                                            self.camNode,
                                            self.render,
                                            self.terrainInfo.terrainCenter )
        self.cameraButtons = CameraButtons( self.terrainCamera )
        self.lights = Lights( self.render )
        self.terrainCollision = TerrainCollision( self.terrain )
        self.terrainCollision.createTerrainCollision()
        self.task_duration = 0.5
        #self.accept( 'mouse1', self.on_map_click )
       # self.taskMgr.add( self.check_camera_movement, 'checkCameraMovement' )
        self.taskMgr.add( self.updateMouseTask, 'updateMouseTask' )
        # Start a task to update the camera position
        self.taskMgr.add( self.terrainCamera.updateCameraTask, "UpdateCameraTask" )

    def on_map_click( self ):
        self.terrainCamera.on_map_click()

    def updateMouseTask( self, task ):
        if not self.terrainCamera.isCenterdOnPoly():
            return task.again
        self.update_mouse_picker()
        task.delayTime = self.task_duration
        return task.again

    def update_mouse_picker( self ):
        self.terrainCamera.on_map_hover()

    def check_camera_movement( self, task ):
        return self.camera.getPos() == self.terrainCamera.center
        # Reschedule the task to check again
        return task.cont


app = MyApp()
app.run()
