from collections import deque
from math import cos, sin, radians
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import Vec3

from entities.locatorMode import LocatorModes
from entities.modules.chassis import Chassis
from entities.parts.engine import Engine
from entities.entity import Entity, entitypart, entitymodule
from entities.parts.part import Part
from enums.colors import Color
from movement.movementmanager import MovementManager
from selectionitem import SelectionItem
from selectionmodes import SelectionModes
from sphere import create_sphere
from statemachine.state import State
from states.bypassstate import BypassState
from states.idlestate import IdleState
from states.movementstate import MovementState
from states.obstaclestate import ObstacleState


class Mover( Entity ):

	def __init__( self, engine, chassis: Chassis ):
		super().__init__()
		self.locatorMode: LocatorModes = LocatorModes.All
		self.angle_increment = 1
		self.angle = 0
		self.__dynamicDetector = None
		self.targetOnly = False
		self.__speed = None
		self.__targetVisible = False
		self.__edge = None
		self.__rightEdge = None
		self.__modelBounds = None
		self.__leftDetector = None
		self.__rightDetector = None
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
		self.__obstacle: 'Entity' | None = None
		self.__lastObstacle: 'Entity' = None
		self.__bypassTarget = None

	@property
	def bpTarget( self ):
		return self.__bypassTarget

	@property
	def speed( self ) -> float:
		return self.__speed

	@speed.setter
	def speed( self, value ):
		self.__speed = value

	@bpTarget.setter
	def bpTarget( self, target ):
		self.__bypassTarget = target

	@property
	def moveTargets( self ) -> deque:
		return self._moveTargets

	@property
	def obstacle( self ):
		return self.__obstacle

	@obstacle.setter
	def obstacle( self, obstacle ):
		if obstacle is not None:
			self.__lastObstacle = obstacle
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
		return self._length

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

	def getDynamicDetectorDirection( self ):
		dynamicPos = self.__dynamicDetector.get_pos( self.render )
		edgePos = self.edgePos()
		return edgePos, dynamicPos

	@property
	def collisionBox( self ):
		return self._partBuilder.collisionBox

	def monitorIdleState( self, task ):
		if not any( self.moveTargets ) and not self.bpTarget:
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
				"obstacle": ObstacleState( self ),
				"bypass": BypassState( self )
		}

	def scheduleTargetMonitoringTask( self ):
		if not taskMgr.hasTaskNamed( f"{ self.name }_target_monitor" ):
			self.scheduleTask( self.targetMonitoringTask )

	def targetMonitoringTask( self, task ):
		if self.__bypassTarget:
			if self._currentTarget in self._selectedTargets:
				self.moveTargets.appendleft( self._currentTarget )
				self._currentTarget.handleSelection( mode = SelectionModes.TEMP )
			else:
				self._currentTarget.clearSelection()
			self._currentTarget = self.__bypassTarget
			self.__bypassTarget = None
		if self._currentTarget is not None:
			return task.cont
		elif any( self.moveTargets ):
			self._currentTarget = self.moveTargets.popleft()
			print( f"current target: {self._currentTarget}" )
		return task.cont

	@property
	def terrainSize( self ):
		return self.__terrainSize

	@terrainSize.setter
	def terrainSize( self, terrainSize ):
		self.__terrainSize = terrainSize

	def schedulePointToPointTasks( self ):
		self._currentTarget.handleSelection( mode = SelectionModes.TARGET )
		position = self._currentTarget.position
		print( f"new position: { position }" )
		self.scheduleTask( self._movementManager.set_velocity_toward_point_with_stop, extraArgs = [ position ] )
		self.scheduleTask( self._movementManager.track_target_angle, checkExisting = True )
		self.scheduleTask( self._movementManager.maintain_terrain_boundaries, extraArgs = [ self.__terrainSize ] )
		self.scheduleTask( self._movementManager.monitor_obstacles )
		self.scheduleTask( self._movementManager.maintain_turret_angle )

	def scheduleObstacleTasks( self ):
		self.scheduleTask( self._movementManager.monitor_handle_obstacles )
		self.scheduleTask( self._movementManager.alternative_target )

	#def scheduleStuckTasks( self ):

	def finishedMovement( self ):
		return self._currentTarget is None

	def hasObstacles( self ) -> bool:
		if self.__obstacle is not None:
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
		#self.setDamping()
		self.connectModules( physicsWorld )
		self.__createModelBounds()
		self.__createEdges()
		self.__createRearEdges()
		self.initMovementManager( physicsWorld )
		self.createStateMachine()

	def clearCurrentTarget( self ):
		if not self._currentTarget:
			return
		self._currentTarget.clearSelection()
		self._currentTarget = None
		if self._currentTarget in self._selectedTargets:
			self._selectedTargets.remove( self._currentTarget )

	def __createEdges( self ):
		self.__edge = create_and_setup_sphere( self.coreBodyPath, Color.RED, Vec3( self._length / 2, 0, 0 ) )
		self.__leftEdge = create_and_setup_sphere( self.coreBodyPath, Color.CYAN, Vec3( self._length / 2, self._width / 2, 0 ) )
		self.__rightEdge = create_and_setup_sphere( self.coreBodyPath, Color.CYAN, Vec3( self._length / 2, - self._width / 2, 0 ) )
		self.__leftDetector = create_and_setup_sphere( self.coreBodyPath, Color.RED, Vec3( self._length, self._width / 2, 0 ) )
		self.__rightDetector = create_and_setup_sphere( self.coreBodyPath, Color.BLUE, Vec3( self._length, - self._width / 2, 0 ) )
		self.__dynamicDetector = create_and_setup_sphere( self.coreBodyPath, Color.YELLOW, Vec3( 0, 0, 0 ) )
		taskMgr.add( self.moveDynamicDetector, "CircularMotionTask" )

	def __createModelBounds( self ):
		self.__modelBounds = self.coreBodyPath.getTightBounds()
		self._width = (self.__modelBounds[ 1 ].y - self.__modelBounds[ 0 ].y)
		self._length = (self.__modelBounds[ 1 ].x - self.__modelBounds[ 0 ].x)
		self._height = (self.__modelBounds[ 1 ].z - self.__modelBounds[ 0 ].z)

	def __createRearEdges( self ):
		self.__leftRearEdge = create_and_setup_sphere( self.coreBodyPath, Color.CYAN, Vec3( -self._length / 2, self._width / 2, 0 ) )
		self.__rightRearEdge = create_and_setup_sphere( self.coreBodyPath, Color.CYAN, Vec3( -self._length / 2, - self._width / 2, 0 ) )
		self.__leftRearDetector = create_and_setup_sphere( self.coreBodyPath, Color.RED, Vec3( -self._length, self._width / 2, 0 ) )
		self.__rightRearDetector = create_and_setup_sphere( self.coreBodyPath, Color.BLUE, Vec3( -self._length, - self._width / 2, 0 ) )

	def moveDynamicDetector( self, task ):
		task.delayTime = 1
		self.angle += self.angle_increment
		if self.angle >= 90 or self.angle <= -90:
			self.angle_increment *= -1
		radians_angle = radians( self.angle )
		x = self._length / 2 + self._width * cos( radians_angle )
		y = self._width * sin( radians_angle )
		z = -1
		self.__dynamicDetector.setPos( x, y, z )
		return task.cont

	def isMidRangeFromObstacle( self ):
		if self.__lastObstacle is None:
			return True
		distance = ( self.__lastObstacle.position - self.position ).length()
		if distance > 100:
			return True
		return False

	def isTargetVisible( self ):
		return self.__targetVisible


def create_and_setup_sphere( parent, color, position, radius = 5.0, slices = 16, stacks = 8 ):
	sphere = create_sphere( radius = radius, slices = slices, stacks = stacks )
	sphere.reparentTo( parent )
	sphere.setColor( color )
	sphere.setPos( position )
	return sphere
