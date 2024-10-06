from direct.task import Task
from panda3d.core import CollisionHandlerQueue, CollisionTraverser,Vec3

from buttons.entitybuttons import EntityButtons
from entities.entity import Entity
from entities.full.movers.tank import Tank
from entities.parts.engine import BasicEngine
from enums.colors import Color

from lights import Lights
from phyisics import globalClock
from picker import Picker
from camera import TerrainCamera
from panda3d.bullet import BulletDebugNode, BulletWorld
from buttons.camerabuttons import CameraButtons
from selector.selector import Selector
from terrainrigidbody import TerrainRigidBody
from selector.terrainselector import TerrainSelector
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
		self.physics_world.setGravity( Vec3( 0, 0, -9.81 ) )
		#self.enable_debug_visualization()
		self.createCollisionLayer( terrain = self.terrain )
		self.terrainPhysicsLayer = self.createPhysicsLayer( blockSize = 128 )

		self.__selector = Selector(
				terrain = self.terrain,
				picker = Picker( self.camera ),
				mouseWatcherNode = self.mouseWatcherNode,
				camNode = self.camNode,
				terrainCamera = self.terrainCamera,
				physicsWorld = self.physics_world,
				render = self.render )
		self.entityButtons = EntityButtons( selector = self.__selector )
		engine = BasicEngine()
		turret = CannonTurret()
		mobility = BasicTracks()
		self.tank = Tank( engine = engine, turret = turret, mobility = mobility )
		self.tank.buildModels( self.loader )

		self.task_duration = 0.2
		self.accept( 'mouse1', self.on_map_click )
		self.accept( 'mouse3', self.on_map_loader_click )
		#self.taskMgr.add( self.updateMouseTask, 'updateMouseTask' )
		self.taskMgr.add( self.terrainCamera.updateCameraTask, "UpdateCameraTask" )
		#self.taskMgr.add( self.check_collisions, "check_collisions" )
		self.taskMgr.add( self.update_physics, "update_physics" )
		#self.taskMgr.doMethodLater( 0.02 ,self.check_collisions ,'check_collisions' )
		self.taskMgr.doMethodLater( 0.02, self.update_physics, 'update_physics' )

		self.terrainCamera.hoverAbove()

	def __createCollisionForEntity( self, entity: Entity ):
		self.collision_handler = CollisionHandlerQueue()
		self.cTrav = CollisionTraverser()
		for col in entity.collisionSystems:
			self.cTrav.addCollider( col, self.collision_handler )

	def on_map_click( self ):
		self.__selector.on_map_click()

	def on_map_loader_click( self ):
		self.__selector.on_map_loader_click( self.tank )

	def updateMouseTask( self, task ):
		self.update_mouse_hover()
		task.delayTime = self.task_duration
		# Return task.again to schedule the task with the new delay
		return Task.again

	def update_mouse_hover( self ):
		self.__selector.on_map_hover()

	def enable_debug_visualization( self ):
		debug_node = BulletDebugNode( 'Debug' )
		debug_node.showWireframe( True )
		debug_node.showBoundingBoxes( True )
		debug_np = self.render.attachNewNode( debug_node )
		debug_np.setColor( Color.RED.value )
		debug_np.show()
		self.physics_world.setDebugNode( debug_np.node() )

	def check_collisions( self, task ):
		"""Check for collisions and print results."""
		self.cTrav.traverse( self.render )
		return task.cont

	def update_physics( self, task ):
		"""Update the physics world."""
		dt = globalClock.getDt()
		self.physics_world.doPhysics( dt )
		return task.cont

	def createPhysicsLayer( self, blockSize ):
		terrainProvider = TerrainProvider( self.loader )
		terrainInfo = terrainProvider.create_terrain( "heightmap1", blockSize = blockSize )
		self.terrainPhysicsLayer = TerrainRigidBody( terrainInfo.terrain, self.physics_world )
		self.terrainPhysicsLayer.createTerrainRigidBody()

	def createCollisionLayer( self, terrain ):
		self.terrainCollisionLayer = TerrainCollision( terrain )
		self.terrainCollisionLayer.createTerrainCollision()


app = MyApp()
app.run()
