from collections import deque

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
		self.__leftEdge = None
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
		self.__bpTarget = None

	@property
	def bpTarget( self ):
		return self.__bpTarget

	@bpTarget.setter
	def bpTarget( self, target ):
		self.__bpTarget = target

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

	def getLeftDetectorDirection( self ):
		leftPos = self.__leftDetector.get_pos( self.render )
		edgePos = self.__leftEdge.get_pos( self.render )
		return edgePos, leftPos

	def getRightDetectorDirection( self ):
		rightPos = self.__rightDetector.get_pos( self.render )
		edgePos = self.__rightEdge.get_pos( self.render )
		return edgePos, rightPos

	@property
	def collisionBox( self ):
		return self._partBuilder.collisionBox

	def monitorIdleState( self, task ):
		if not any( self.selectTargets ) and not self.bpTarget:
			return task.cont
		print( f'{self.name} new targets' )
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
		if self.__bpTarget:
			self.selectTargets.appendleft( self._currentTarget )
			self._currentTarget = self.__bpTarget
			self.__bpTarget = None
		elif any( self.selectTargets ):
			self._currentTarget = self.selectTargets.popleft()
		print( f"current target: {self._currentTarget}" )
		self._currentTarget.handleSelection( mode = SelectionModes.TARGET )
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
		if self.__obstacle != None:
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
		self.__modelBounds = self.coreBodyPath.getTightBounds()
		self._width = (self.__modelBounds[ 1 ].y - self.__modelBounds[ 0 ].y)
		self._height = (self.__modelBounds[ 1 ].x - self.__modelBounds[ 0 ].x)

		self.__edge = create_and_setup_sphere(
				self.coreBodyPath, Color.RED, Vec3( self._height / 2, 0, 0 )
		)

		self.__leftEdge = create_and_setup_sphere(
				self.coreBodyPath, Color.CYAN, Vec3( self._height / 2, self._width / 2, 0 )
		)
		self.__rightEdge = create_and_setup_sphere(
				self.coreBodyPath, Color.CYAN, Vec3( self._height / 2, - self._width / 2, 0 )
		)
		self.__leftDetector = create_and_setup_sphere(
				self.coreBodyPath, Color.BLUE, Vec3( self._height, self._width / 2, 0 )
		)
		self.__rightDetector = create_and_setup_sphere(
				self.coreBodyPath, Color.BLUE, Vec3( self._height, - self._width / 2, 0 )
		)


def create_and_setup_sphere( parent, color, position, radius = 5.0, slices = 16, stacks = 8 ):
	sphere = create_sphere( radius = radius, slices = slices, stacks = stacks )
	sphere.reparentTo( parent )
	sphere.setColor( color )
	sphere.setPos( position )
	return sphere
