from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import Vec3

from entities.modules.chassis import Chassis
from entities.parts.engine import Engine
from entities.entity import Entity, entitypart, entitymodule
from entities.parts.part import Part
from enums.colors import Color
from movement.movementmgr import MovementManager
from selectionitem import SelectionItem
from selectionmodes import SelectionModes
from sphere import create_sphere
from statemachine.state import State
from states.idlestate import IdleState
from states.movementstate import MovementState
from states.obstaclestate import ObstacleState


class Mover( Entity ):

	def __init__( self, engine, chassis: Chassis ):
		super().__init__()
		self.__modelBounds = None
		self.__leftDetector = None
		self.__rightDetector = None
		self._height = None
		self._width = None
		self.__edge = None
		self._movementManager = None
		self.__hpr = None
		self.regularSpeed = 100
		self._chassis = chassis
		self._currentPosition = None
		self._engine = engine
		self._mobility = chassis.mobility()
		self._hull = chassis.hull()
		self._corePart = self.mobility()
		self._isMover = True
		self._currentTarget = None
		self.__terrainSize = None
		self.__obstacle = None

	@property
	def obstacle( self ):
		return self.__obstacle

	@obstacle.setter
	def obstacle( self, obstacle ):
		self.__obstacle = obstacle

	@property
	def currentTarget( self ) -> SelectionItem:
		return self._currentTarget

	@property
	def hpr( self ) -> Vec3:
		if self.coreBodyPath:
			return Vec3( self.coreBodyPath )

	@property
	def width( self ):
		return self._width

	@property
	def height( self ):
		return self._height

	def edgePos( self ):
		return self.__edge.get_pos( self.render )

	def getLeftDetectorDirection( self ) -> Vec3:
		leftPos = self.__leftDetector.get_pos( self.render )
		edgePos = self.__edge.get_pos( self.render )
		return Vec3( leftPos.x - edgePos.x, leftPos.y - edgePos.y, 0 )

	def getRightDetectorDirection( self ) -> Vec3:
		rightPos = self.__rightDetector.get_pos( self.render )
		edgePos = self.__edge.get_pos( self.render )
		return Vec3( rightPos.x - edgePos.x, rightPos.y - edgePos.y, 0 )

	@property
	def collisionBox( self ):
		return self._partBuilder.collisionBox

	def monitorIdleState( self, task ):
		if not any( self.selectTargets ):
			return task.cont
		print( f'{ self.name } new targets' )
		return task.done

	def initMovementManager( self, world ):
		self._movementManager = MovementManager( self, world )

	def decide( self, currentState: 'State' ) -> str:
		if currentState == "MovementState":
			return "idle"

	def initStatesPool( self ):
		self._statesPool = {
				"idle": IdleState( self ),
				"movement": MovementState( self ),
				"obstacle": ObstacleState( self )
		}

	def scheduleIdleMonitoringTask( self ):
		pass

	#self.scheduleTask( self.monitorIdleState, "monitoring command" )
	@property
	def terrainSize( self ):
		return self.__terrainSize

	@terrainSize.setter
	def terrainSize( self, terrainSize ):
		self.__terrainSize = terrainSize

	def schedulePointToPointTask( self ):
		self._currentTarget = self.selectTargets.popleft()
		print( f"current target: {self._currentTarget}" )
		position = self._currentTarget.position
		self.scheduleTask(
				self._movementManager.set_velocity_toward_point_with_stop,
				f"{self.name}_move_p2p",
				extraArgs = [ position ],
				appendTask = True
		)
		if not taskMgr.hasTaskNamed( f"{self.name}_monitor_angle" ):
			self.scheduleTask(
					self._movementManager.track_target_angle,
					f"{self.name}_monitor_angle",
					appendTask = True
			)
		self.scheduleTask(
				self._movementManager.maintain_terrain_boundaries,
				f"{self.name}_maintain_boundaries",
				extraArgs = [ self.__terrainSize ],
				appendTask = True
		)
		self.scheduleTask(
				self._movementManager.monitor_obstacles,
				f"{self.name}_monitor_obstacles",
				appendTask = True
		)
		self.scheduleTask(
				self._movementManager.maintain_turret_angle,
				f"{self.name}_maintain_turret_angle",
				extraArgs = [ position ],
				appendTask = True
		)

	def scheduleObstacleTasks( self ):
		self.scheduleTask(
				self._movementManager.monitor_handle_obstacles,
				f"{self.name}monitor_obstacles_1",
				appendTask = True
		)
		self.scheduleTask(
				self._movementManager.alternative_target,
				f"{self.name}handle_obstacle2",
				appendTask = True
		)

	def finishedMovement( self ):
		if taskMgr.hasTaskNamed( f"{self.name}_move_p2p" ):
			return False
		return True

	def hasObstacles( self ) -> bool:
		if self.obstacle != None:
			return True
		return False

	@entitypart
	def hull( self ) -> Part:
		return self._hull

	@entitypart
	def mobility( self ) -> Part:
		return self._mobility

	@entitymodule
	def chassis( self ) -> Chassis:
		return self._chassis

	#   @entitypart
	def engine( self ) -> Engine:
		return self._engine

	def _maintainTurretAngle( self, target ):
		raise NotImplementedError

	def selfHit( self, hit ):
		return hit in self._partBuilder.rigidBodyNodes

	def completeLoading( self, physicsWorld ):
		self.setDamping()
		self.connectModules( physicsWorld )
		self.createEdges()
		self.createStateMachine()
		self.initMovementManager( physicsWorld )

	@currentTarget.setter
	def currentTarget( self, value ):
		self._currentTarget = value

	def displayTargets( self ):
		print( self._selectTargets )

	def createEdges( self ):
		self.__edge = create_sphere( radius = 5.0, slices = 16, stacks = 8 )
		self.__modelBounds = self.coreBodyPath.getTightBounds()
		self._width = ( self.__modelBounds[ 1 ].y - self.__modelBounds[ 0 ].y )
		self._height = ( self.__modelBounds[ 1 ].x - self.__modelBounds[ 0 ].x )
		self.__edge.reparentTo( self.coreBodyPath )
		self.__edge.setColor( Color.CYAN )
		self.__edge.setPos( Vec3( ( self.__modelBounds[ 1 ].x - self.__modelBounds[ 0 ].x ) / 2, 0, 0 ) )
		self.__leftDetector = create_sphere( radius = 5.0, slices = 16, stacks = 8 )
		self.__leftDetector.reparentTo( self.coreBodyPath )
		self.__leftDetector.setColor( Color.BLUE )
		self.__leftDetector.setPos( ( self.__modelBounds[ 1 ].x - self.__modelBounds[ 0 ].x ), ( self.__modelBounds[ 1 ].y - self.__modelBounds[ 0 ].y ) / 4, 0 )
		self.__rightDetector = create_sphere( radius = 5.0, slices = 16, stacks = 8 )
		self.__rightDetector.reparentTo( self.coreBodyPath )
		self.__rightDetector.setColor( Color.BLUE )
		self.__rightDetector.setPos( ( self.__modelBounds[ 1 ].x - self.__modelBounds[ 0 ].x ),  ( self.__modelBounds[ 0 ].y - self.__modelBounds[ 1 ].y ) / 4, 0 )

	def relocateDetectors( self, denominator: int = 4 ):
		for detector in [ self.__leftDetector, self.__rightDetector ]:
			self.__rightDetector.setPos( ( self.__modelBounds[ 1 ].x - self.__modelBounds[ 0 ].x ),
			                             ( self.__modelBounds[ 0 ].y - self.__modelBounds[ 1 ].y) / denominator, 0 )
