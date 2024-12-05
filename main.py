import threading

from direct.task import Task
from panda3d.core import CollisionHandlerQueue, CollisionTraverser,Vec3

from buttons.entitybuttons import EntityButtons
from entities.entity import Entity
from entityloader import EntityLoader
from enums.colors import Color

from lights import Lights
from phyisics import globalClock
from picker import Picker
from camera.camera import TerrainCamera
from panda3d.bullet import BulletDebugNode, BulletWorld
from buttons.camerabuttons import CameraButtons
from selector.selector import Selector
from terrainrigidbody import TerrainRigidBody
from terraincolision import TerrainCollision
from direct.showbase.ShowBase import ShowBase
from maps.terrainprovider import TerrainProvider
import sys
sys.dont_write_bytecode = True


class MyApp( ShowBase ):

	def __init__( self ):

		ShowBase.__init__( self )
		self.__terrainPhysicsLayer = None
		self.__terrainCollisionLayer = None
		self.__createTerrain()
		self.disableMouse()
		# Set up Bullet physics world
		self.physics_world = BulletWorld()
		self.physics_world.setGravity( Vec3( 0, 0, -9.81 ) )
		self.physics_world.setGroupCollisionFlag( 1, 1, False )
		self.terrainCamera = TerrainCamera( self.camera, self.terrainInfo.terrainCenter, self.terrainInfo.terrainSize )
		self.cameraButtons = CameraButtons( self.terrainCamera, debugNode = self.get_debug_visualization() )
		self.lights = Lights( self.render )
		self.__createCollisionLayer( terrain = self.terrain )
		self.__createPhysicsLayer( blockSize = 32 )

		self.__selector = Selector(
				picker = Picker( self.camera ),
				mouseWatcherNode = self.mouseWatcherNode,
				camNode = self.camNode,
				terrainCamera = self.terrainCamera,
				render = self.render )
		self.__entityLoader = EntityLoader( render = self.render, physicsWorld = self.physics_world, loader = self.loader, taskMgr = self.taskMgr )
		self.entityButtons = EntityButtons( selector = self.__selector, loader = self.__entityLoader, taskMgr = self.taskMgr )

		self.task_duration = 0.2
		self.accept( 'mouse1', self.on_map_click )
		#self.taskMgr.add( self.updateMouseTask, 'updateMouseTask' )
		self.taskMgr.add( self.terrainCamera.updateCameraTask, "UpdateCameraTask" )
		#self.taskMgr.add( self.check_collisions, "check_collisions" )
		self.taskMgr.add( self.update_physics, "update_physics" )
		#self.taskMgr.doMethodLater( 0.02 ,self.check_collisions ,'check_collisions' )
		self.taskMgr.doMethodLater( 0.02, self.update_physics, 'update_physics' )
		self.terrainCamera.hoverAbove()
		self.start_command_listener()

	def __createTerrain( self ):
		terrainProvider = TerrainProvider( self.loader )
		self.terrainInfo = terrainProvider.create_terrain( "heightmap_flat" )
		self.terrain = self.terrainInfo.terrain
		self.terrain.getRoot().reparentTo( self.render )
		self.terrain.setFocalPoint( self.camera )

	def start_command_listener( self ):
		threading.Thread( target = self.command_listener, daemon = True ).start()

	def command_listener( self ):
		while True:
			command = input( "Enter a command: " ).strip()
			if command.startswith( "rotate" ):
				self.rotate_entity()

	def rotate_entity( self,  degrees = 120 ):
		self.__selector.selectedMover.rotate( degrees )
		print( "Action triggered from terminal command!" )

	def __createCollisionForEntity( self, entity: Entity ):
		self.collision_handler = CollisionHandlerQueue()
		self.cTrav = CollisionTraverser()
		for col in entity.collisionSystems:
			self.cTrav.addCollider( col, self.collision_handler )

	def on_map_click( self ):
		self.__selector.on_map_click()

	def updateMouseTask( self, task ):
		self.update_mouse_hover()
		task.delayTime = self.task_duration
		return Task.again

	def update_mouse_hover( self ):
		self.__selector.on_map_hover()

	def get_debug_visualization( self ):
		debug_node = BulletDebugNode( 'Debug' )
		debug_node.showWireframe( True )
		debug_node.showBoundingBoxes( True )
		debug_np = self.render.attachNewNode( debug_node )
		debug_np.setColor( Color.RED.value )
		#debug_np.show()
		self.physics_world.setDebugNode( debug_np.node() )
		return debug_np

	def check_collisions( self, task ):
		self.cTrav.traverse( self.render )
		return task.cont

	def update_physics( self, task ):
		dt = globalClock.getDt()
		self.physics_world.doPhysics( dt )
		return task.cont

	def __createPhysicsLayer( self, blockSize ):
		terrainProvider = TerrainProvider( self.loader )
		terrainInfo = terrainProvider.create_terrain( "heightmap_flat", blockSize = blockSize )
		self.__terrainPhysicsLayer = TerrainRigidBody( terrainInfo.terrain, self.physics_world )
		self.__terrainPhysicsLayer.createTerrainRigidBody()

	def __createCollisionLayer( self, terrain ):
		self.__terrainCollisionLayer = TerrainCollision( terrain )
		self.__terrainCollisionLayer.createTerrainCollision()


app = MyApp()
app.run()
