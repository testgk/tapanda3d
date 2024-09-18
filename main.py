from direct.task import Task
from panda3d.core import Vec3

from entities.full.movers.tank import Tank
from entities.parts.engine import BasicEngine

from lights import Lights
from picker import Picker
from camera import TerrainCamera
from panda3d.bullet import BulletWorld
from camerabuttons import CameraButtons
from terrainselector import TerrainSelector
from terraincolision import TerrainCollision
from direct.showbase.ShowBase import ShowBase
from entities.parts.mobility import BasicTracks
from entities.modules.turret import CannonTurret
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
        self.terrainCamera = TerrainCamera( self.camera, self.terrainInfo.terrainCenter, self.terrainInfo.terrainSize )
        self.cameraButtons = CameraButtons( self.terrainCamera )
        self.lights = Lights( self.render )
        self.terrainCollision = TerrainCollision( self.terrain )

        # Set up Bullet physics world
        self.physics_world = BulletWorld()
        self.physics_world.setGravity(Vec3(0, 0, -9.81))
        terrain_np = self.render.attachNewNode( self.terrainInfo.rigidBodyNode )
        terrain_np.setPos(0, 0, 0)
        self.physics_world.attachRigidBody( self.terrainInfo.rigidBodyNode )

        self.terrainSelector = TerrainSelector(
            terrain = self.terrain,
            terrainPicker = Picker( self.camera ),
            mouseWatcherNode = self.mouseWatcherNode,
            camNode =  self.camNode,
            terrainCamera = self.terrainCamera,
            physicsWorld = self.physics_world,
            taskMgr = self.taskMgr,
            render = self.render )

        engine = BasicEngine()
        turret = CannonTurret()
        mobility = BasicTracks()
        self.tank = Tank( engine = engine, turret = turret, mobility = mobility )
        self.tank.buildModels( self.loader )


        self.task_duration = 0.2
        self.accept( 'mouse1', self.on_map_click )
        self.accept( 'mouse3', self.on_map_loader_click )
        self.terrainCollision.createTerrainCollision()
        self.taskMgr.add( self.updateMouseTask, 'updateMouseTask' )
        self.taskMgr.add( self.terrainCamera.updateCameraTask, "UpdateCameraTask" )
        self.terrainCamera.hoverAbove()

    def on_map_click( self ):
        self.terrainSelector.on_map_click()

    def on_map_loader_click( self ):
        for model in self.tank.models:
            self.terrainSelector.on_map_loader_click( model )

    def updateMouseTask( self, task ):
        self.update_mouse_hover()
        task.delayTime = self.task_duration
        # Return task.again to schedule the task with the new delay
        return Task.again

    def update_mouse_hover( self ):
        self.terrainSelector.on_map_hover()


app = MyApp()
app.run()
