from direct.task import Task
from panda3d.core import CollisionHandlerQueue, CollisionTraverser,Vec3

from buttons.entitybuttons import EntityButtons
from entities.entity import Entity
from entityloader import EntityLoader
from enums.colors import Color

from lights import Lights
from phyisics import globalClock
from picker import Picker
from camera import TerrainCamera
from panda3d.bullet import BulletDebugNode, BulletWorld
from buttons.camerabuttons import CameraButtons
from selector.selector import Selector
from terrainrigidbody import TerrainRigidBody
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
		# Set up Bullet physics world
		self.physics_world = BulletWorld()
		self.physics_world.setGravity( Vec3( 0, 0, -9.81 ) )
		self.physics_world.setGroupCollisionFlag( 1, 1, False )
		self.terrainCamera = TerrainCamera( self.camera, self.terrainInfo.terrainCenter, self.terrainInfo.terrainSize )
		self.cameraButtons = CameraButtons( self.terrainCamera, debugNode = self.get_debug_visualization() )
		self.lights = Lights( self.render )
		self.createCollisionLayer( terrain = self.terrain )
		self.createPhysicsLayer( blockSize = 128 )

		self.__selector = Selector(
				terrain = self.terrain,
				picker = Picker( self.camera ),
				mouseWatcherNode = self.mouseWatcherNode,
				camNode = self.camNode,
				terrainCamera = self.terrainCamera,
				physicsWorld = self.physics_world,
				render = self.render )
		self.__entityLoader = EntityLoader( render = self.render, physicsWorld = self.physics_world, loader = self.loader )
		self.entityButtons = EntityButtons( selector = self.__selector, loader = self.__entityLoader )


		self.task_duration = 0.2
		self.accept( 'mouse1', self.on_map_click )
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
