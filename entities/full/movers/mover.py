from abc import abstractmethod

from panda3d.core import Vec3
from collections import deque
from moverdetectors import Detectors
from entities.modules.mobilechassis import MobileChassis
from target import Target
from states.states import States
from statemachine.state import State
from entities.parts.part import Part
from selectionmodes import SelectionModes
from states.mover.backupstate import BackupState
from states.mover.checkobstaclestate import CheckObstacle
from movement.movementmanager import MovementManager
from entities.entity import Entity, entitypart
from panda3d.bullet import BulletSphereShape, BulletRigidBodyNode
from entities.locatorMode import LocatorModes, LocatorLength, Locators
from states import ( MovementState, CautiousState, CurveIdleState, CurveMovementState,
                    ObstacleState, IdleState, GenerateCurveState, GenerateBypassState )



class MovingEntity:

	@abstractmethod
	def mobility( self ) -> Part:
		pass

	@property
	@abstractmethod
	def speed( self ) -> float:
		pass


class Mover( Entity, MovingEntity ):
	def __init__( self, engine, chassis: MobileChassis ):
		super().__init__()
		self.__render = None
		self.__curveTarget = None
		self.__aligned: bool = False
		self.__nextTarget = None
		self.locatorMode: LocatorModes = LocatorModes.All
		self.detectorLength: LocatorLength = LocatorLength.Medium
		self.__speed = None
		self.__targetVisible = False
		self.__modelBounds = None
		self._movementManager: MovementManager or None = None
		self.__hpr = None
		self.regularSpeed = 100
		self._currentPosition = None
		self._engine = engine
		self._mobility = chassis.mobility()
		self._hull = chassis.hull()
		self._corePart = self.mobility()
		self._isMover = True
		self.__currentTarget = None
		self.__terrainSize = None
		self.__obstacle: 'Entity' or None = None
		self.__lastObstacle: 'Entity' or None = None
		self.__bypassTarget: Target or None = None
		self.__curveTargets: list[ Target ] = []
		self.__stopDistance = True
		self.__detectors = None


	@property
	def bypassTarget( self ):
		return self.__bypassTarget

	@property
	def curveTarget( self ):
		return self.__curveTarget

	@bypassTarget.setter
	def bypassTarget( self, target: Target ):
		self.__bypassTarget = target

	@property
	def insideCurve( self ):
		return any( self.__curveTargets )

	@property
	def speed( self ) -> float:
		return self.__speed

	@speed.setter
	def speed( self, value ):
		self.__speed = value

	@property
	def aligned( self ):
		return self.__aligned

	@aligned.setter
	def aligned( self, value ):
		self.__aligned = value

	@property
	def moveTargets( self ) -> deque:
		return self._moveTargets

	@property
	def stopDistance(self):
		return self.__stopDistance

	@stopDistance.setter
	def stopDistance(self, value):
		self.__stopDistance = value

	@property
	def detectors( self ) -> Detectors:
		return self.__detectors

	@property
	def obstacle( self ):
		return self.__obstacle

	@obstacle.setter
	def obstacle( self, obstacle ):
		if obstacle is not None:
			self.__lastObstacle = obstacle
		self.__obstacle = obstacle

	@property
	def currentTarget( self ) -> Target:
		return self.__currentTarget

	@property
	def hpr( self ) -> Vec3:
		if self.coreBodyPath:
			return Vec3( self.coreBodyPath )

	def __initMovementManager( self, world ):
		self._movementManager = MovementManager( self, world, self.__render )

	def decide( self, currentState: 'State' ) -> str | None:
		if currentState is MovementState:
			return States.IDLE

	def _initStatesPool( self ):
		self._statesPool = {
				States.IDLE: IdleState( self ),
				States.MOVEMENT: MovementState( self ),
				States.OBSTACLE: ObstacleState( self ),
				States.CAUTIOUS: CautiousState( self ),
				States.BYPASS: GenerateBypassState( self ),
				States.CHECK_OBSTACLE: CheckObstacle( self ),
				States.BACKUP: BackupState( self ),
				States.CURVE: GenerateCurveState( self ),
				States.CURVE_MOVEMENT: CurveMovementState( self ),
				States.CURVE_IDLE: CurveIdleState( self )
		}

	def scheduleTargetMonitoringTask( self ):
		self.scheduleTask( self.targetMonitoringTask, checkExisting = True )

	def scheduleCurveMovementMonitoringTaskTask( self ):
		self.scheduleTask( self.curveMovementMonitoringTask, checkExisting = True )

	def curveMovementMonitoringTask( self, task ):
		if not any( self.__curveTargets ):
			return task.done

		#if self.hasObstacles():
		#	return task.done

		if self.__currentTarget is None and any( self.__curveTargets ):
			self.__currentTarget = self.__curveTargets.pop()
		return task.cont

	def byPassMovementMonitoringTask( self, task ):
		if self.__currentTarget:
			return task.cont

		if any( self.moveTargets ):
			self.__currentTarget = self.moveTargets.pop()
			self.__currentTarget.handleSelection( mode = SelectionModes.P2P )
			return task.cont

		return task.done

	def targetMonitoringTask( self, task ):
		#if self.__bypassTarget:
		#	return task.done

		if any( self.__curveTargets ):
			return task.done

		if self.bypassTarget:
			self.__curveTarget = self.bypassTarget
			return task.done

		# accept new selected target
		if self.__nextTarget is None and any( self._selectedTargets ):
			self.__nextTarget = self._selectedTargets.pop()

		if self.__currentTarget is not None:
			return task.cont

		if self.__nextTarget is not None and self.__nextTarget not in self.moveTargets:
			self.moveTargets.append( self.__nextTarget )

		# accept target from existing move targets
		if any( self.moveTargets ):
			self.__currentTarget = self.moveTargets.pop()
			print( f"current target: { self.__currentTarget }" )
			self.__currentTarget.handleSelection( mode = SelectionModes.P2P )

		return task.cont

	@property
	def terrainSize( self ):
		return self.__terrainSize

	@terrainSize.setter
	def terrainSize( self, terrainSize ):
		self.__terrainSize = terrainSize

	def schedulePointToPointTasks( self ):
		self.scheduleTask( self._movementManager.set_velocity_toward_point_with_stop, checkExisting = True )
		self.scheduleTask( self._movementManager.track_target_coreBody_angle, checkExisting = True )
		self.scheduleTask( self._movementManager.maintain_terrain_boundaries, extraArgs = [ self.__terrainSize ] )
		self.scheduleTask( self._movementManager.monitor_obstacles )
		self.scheduleTask( self._movementManager.maintain_turret_angle )

	def generateCurve( self ):
		pos1 = self.position
		pos2 = self.__curveTarget.position
		pos3 = self.__nextTarget.position
		if self._movementManager.generateAndCheckNewCurve( positions = [ pos1, pos2, pos3 ], obstacle = self.__obstacle ):
			targets = self._movementManager.getCurvePoints()
			self.__curveTargets = targets[ ::20 ]
			self.__curveTarget = None
			self.__currentTarget = None
			self.removeObstacle()
			return True
		return False

	def generateBypass( self ):
		self.moveTargets.append( self.__currentTarget )
		self.moveTargets.append( self.__bypassTarget )
		self.__bypassTarget = None
		self.__currentTarget = None

	def scheduleBackupTasks( self ):
		self.scheduleTask( self._movementManager.set_velocity_backwards_direction )
		self.scheduleTask( self._movementManager.monitor_obstacles )

	def scheduleCheckObstaclesTasks( self ):
		self.scheduleTask( self._movementManager.track_target_coreBody_angle, checkExisting = True )
		self.scheduleTask( self._movementManager.monitor_obstacles )

	def scheduleObstacleTasks( self ):
		self.scheduleTask( self._movementManager.target_detection )

	def finishedMovement( self ):
		return self.__currentTarget is None

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

	def selfHit( self, hit ):
		return hit in self._partBuilder.rigidBodyNodes

	def completeLoading( self, physicsWorld, render, terrainSize ) -> None:
		self._setDamping()
		self._connectModules( physicsWorld )
		self._createModelBounds()
		self.__render = render
		self.__terrainSize = terrainSize
		self.__initMovementManager( physicsWorld )
		self._createStateMachine()
		self._setCoreBodyPath()
		self.__detectors = Detectors( self.coreBodyPath, self._length, self._width, self.__render )

	def clearCurrentTarget( self ):
		if not self.__currentTarget:
			return
		if self.__currentTarget is self.__nextTarget:
			self.__nextTarget = None
		self.__currentTarget = None

	def isMidRangeFromObstacle( self ) -> bool:
		if self.__lastObstacle is None:
			return True
		distance = ( self.__lastObstacle.position - self.position ).length()
		if distance > 100:
			return True
		return False

	def closeToObstacle( self ) -> bool:
		if not self.hasObstacles():
			return False
		return self._movementManager.distanceFromObstacle() <= 120

	def setPos( self, pos ) -> None:
		self.coreBodyPath.setPos( pos )

	def selectedTarget( self, target ) -> bool:
		return target is self.__nextTarget or target in self._selectedTargets

	def terminateCurve( self ):
		self._movementManager.terminateCurve()

	def stopMovement( self ):
		self._movementManager.stopMovement()

	def removeObstacle( self ) -> None:
		if self.__obstacle:
			self.__obstacle.clearSelection()
		self.__obstacle = None



