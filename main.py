from lights import Lights
from camera import TerrainCamera
from camerabuttons import CameraButtons
from picker import Picker
from terrainselector import TerrainSelector
from terraincolision import TerrainCollision
from direct.showbase.ShowBase import ShowBase
from maps.terrainprovider import TerrainProvider

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
        self.terrainCamera = TerrainCamera( self.camera, self.terrainInfo.terrainCenter )
        self.cameraButtons = CameraButtons( self.terrainCamera )
        self.lights = Lights( self.render )
        self.terrainCollision = TerrainCollision( self.terrain )
        self.terrainSelector = TerrainSelector(
            terrain = self.terrain,
            terrainPicker = Picker( self.camera ),
            mouseWatcherNode = self.mouseWatcherNode,
            camNode =  self.camNode,
            terrainCamera = self.terrainCamera,
            render = self.render )
        self.task_duration = 0.2
        self.accept( 'mouse1', self.on_map_loader_click )
        self.terrainCollision.createTerrainCollision()
        self.taskMgr.add( self.updateMouseTask, 'updateMouseTask' )
        self.taskMgr.add( self.terrainCamera.updateCameraTask, "UpdateCameraTask" )
        self.terrainCamera.hoverAbove()


    def on_map_click( self ):
        self.terrainSelector.on_map_click()

    def on_map_loader_click( self ):
        model = self.loader.loadModel('objects/tank.egg')
        self.terrainSelector.on_map_loader_click( model )


    def updateMouseTask( self, task ):
        self.update_mouse_hover()
        return task.again

    def update_mouse_hover( self ):
        self.terrainSelector.on_map_hover()


app = MyApp()
app.run()
