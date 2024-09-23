from direct.task import Task
from panda3d.core import CollisionHandlerPusher, CollisionHandlerQueue, CollisionTraverser, LColor, Vec3

from entities.full.movers.tank import Tank
from entities.parts.engine import BasicEngine
from enums.colors import Color

from lights import Lights
from phyisics import globalClock
from picker import Picker
from camera import TerrainCamera
from panda3d.bullet import BulletDebugNode, BulletWorld
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

        # Set up Bullet physics world
        self.physics_world = BulletWorld()
        self.physics_world.setGravity(Vec3(0, 0, -9.81))
        self.enable_debug_visualization()
        self.terrainCollision = TerrainCollision( self.terrain, self.physics_world, self.render )

        #terrain_np = self.render.attachNewNode( self.terrainInfo.rigidBodyNode  )
        #terrain_np.setPos( self.terrain.getRoot().getPos() )
        #self.physics_world.attachRigidBody( self.terrainInfo.rigidBodyNode )
        #terrain_np.show()

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
        self.collision_handler = CollisionHandlerQueue()
        self.cTrav = CollisionTraverser()
        for col in self.tank.collisionSystems:
            self.cTrav.addCollider( col, self.collision_handler )

        self.task_duration = 0.2
        self.accept( 'mouse1', self.on_map_click )
        self.accept( 'mouse3', self.on_map_loader_click )
        self.terrainCollision.createTerrainCollision()
        self.taskMgr.add( self.updateMouseTask, 'updateMouseTask' )
        self.taskMgr.add( self.terrainCamera.updateCameraTask, "UpdateCameraTask" )
        self.taskMgr.add(self.traverse_collisions, "traverse_collisions")
        self.taskMgr.add( self.check_collisions, "check_collisions" )
        self.taskMgr.add( self.update_physics, "update_physics" )
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

    def enable_debug_visualization( self ) :
        """Enables Bullet debug visualization."""
        # Create a BulletDebugNode for visualization
        debug_node = BulletDebugNode( 'Debug' )
        # Show wireframe for collision shapes
        debug_node.showWireframe( True )
        # Optionally show bounding boxes
        debug_node.showBoundingBoxes( True )
        # Attach the debug node to render
        debug_np = self.render.attachNewNode( debug_node )
        debug_np.setColor( Color.RED.value )
        debug_np.show()
        # Attach the debug node to the Bullet world
        self.physics_world.setDebugNode( debug_np.node() )

    def traverse_collisions( self, task ) :
        """Traverse the scene and detect collisions."""
        self.cTrav.traverse( self.render )
        return task.cont

    def check_collisions(self, task):
        """Check for collisions and print results."""
        self.cTrav.traverse(self.render)

        # Go through the collision handler to see if any collisions were detected
        if self.collision_handler.getNumEntries() > 0:
            self.collision_handler.sortEntries()  # Sort by distance
            for entry in self.collision_handler.getEntries():
                print("Collision detected between:", entry.getFromNodePath(), "and", entry.getIntoNodePath())

        return task.cont

    def update_physics(self, task):
        """Update the physics world."""
        dt = globalClock.getDt()
        self.physics_world.doPhysics(dt)
        return task.cont


app = MyApp()
app.run()
