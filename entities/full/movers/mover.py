from abc import abstractmethod, ABC

from target import Target
from panda3d.core import Vec3
from collections import deque
from scheduletask import scheduleTask
from detection.sensors import Senesors
from detection.detector import Detector
from states.statenames import StateNames
from selection.selectionitem import SelectionItem
from selection.selectionmodes import SelectionModes
from movement.movementmanager import MovementManager
from entities.modules.mobilechassis import MobileChassis

from statemachine.state import State
from entities.parts.part import Part

from entities.entity import Entity, entitypart
from entities.locatorMode import LocatorModes, LocatorLength
from states import ( MovementState, CautiousState, CurveIdleState, CurveMovementState, BackupState, CheckObstacle,
                    ObstacleState, IdleState, GenerateCurveState, GenerateBypassState )



class MovingEntity( ABC ):

	@abstractmethod
	def mobility( self ) -> Part:
		pass

	@property
	@abstractmethod
	def speed( self ) -> float:
		pass


class Mover( Entity, MovingEntity, ABC ):
	def __init__( self, engine, chassis: MobileChassis ):
		super().__init__()
		self.__detector = None
		self.__render = None
		self.__curveRootTarget = None
		self.__aligned: bool = False
		self.__nextTarget = None
		self.locatorMode: LocatorModes = LocatorModes.All
		self.detectorLength: int = LocatorLength.Medium
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
		self.__sensors = None


	@property
	def bypassTarget( self ) -> Target or None:
		return self.__bypassTarget

	@property
	def curveRootTarget( self ) -> Target or None:
		return self.__curveRootTarget

	@bypassTarget.setter
	def bypassTarget( self, target: Target ):
		self.__bypassTarget = target

	@property
	def insideCurve( self ) -> bool:
		return any( self.__curveTargets )

	@property
	def speed( self ) -> float:
		return self.__speed

	@speed.setter
	def speed( self, value: int ):
		self.__speed = value

	@property
	def aligned( self ) -> bool:
		return self.__aligned

	@aligned.setter
	def aligned( self, value: bool ):
		self.__aligned = value

	@property
	def moveTargets( self ) -> deque:
		return self._moveTargets

	@property
	def stopAtDistance(self):
		return self.__stopDistance

	@stopAtDistance.setter
	def stopAtDistance(self, value):
		self.__stopDistance = value

	@property
	def sensors( self ) -> Senesors:
		return self.__sensors

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

	def decide( self, currentState: 'State' ) -> str | None:
		if currentState is MovementState:
			return StateNames.IDLE

	def _initStatesPool( self ):
		self._statesPool = {
				StateNames.IDLE: IdleState(self),
				StateNames.MOVEMENT: MovementState(self),
				StateNames.OBSTACLE: ObstacleState(self),
				StateNames.CAUTIOUS: CautiousState(self),
				StateNames.BYPASS: GenerateBypassState(self),
				StateNames.CHECK_OBSTACLE: CheckObstacle(self),
				StateNames.BACKUP: BackupState(self),
				StateNames.CURVE: GenerateCurveState(self),
				StateNames.CURVE_MOVEMENT: CurveMovementState(self),
				StateNames.CURVE_IDLE: CurveIdleState(self)
		}

	def selectItem( self, item: 'SelectionItem' ) -> SelectionItem | None:
		if item == self:
			self.clearSelection()
			return None
		if not item.isTerrain:
			item.handleSelection( SelectionModes.ANY )
			self.clearSelection()
			return item
		else:
			self._selectedTargets.appendleft( item )
			item.handleSelection( SelectionModes.P2P )
			return self

	def scheduleTargetMonitoringTask( self ):
		scheduleTask( self, self.targetMonitoringTask, checkExisting = True )
		scheduleTask( self, self._movementManager.monitor_obstacles )

	def scheduleCurveMovementMonitoringTask( self ):
		scheduleTask( self, self.curveMovementMonitoringTask, checkExisting = True )

	def curveMovementMonitoringTask( self, task ):
		if not any( self.__curveTargets ):
			return task.done

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
		task.delayTime = 0.1
		if any( self.__curveTargets ):
			return task.done

		if self.bypassTarget:
			self.__curveRootTarget = self.bypassTarget
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
			if self.__currentTarget:
				self.__currentTarget.handleSelection( mode = SelectionModes.P2P )
		return task.again

	@property
	def terrainSize( self ):
		return self.__terrainSize

	@terrainSize.setter
	def terrainSize( self, terrainSize ):
		self.__terrainSize = terrainSize

	def schedulePointToPointTasks( self ):
		scheduleTask( self, self._movementManager.set_velocity_toward_point_with_stop, checkExisting = True )
		scheduleTask( self, self._movementManager.track_target_coreBody_angle, checkExisting = True )
		scheduleTask( self, self._movementManager.maintain_terrain_boundaries, extraArgs = [ self.__terrainSize ] )
		scheduleTask( self, self._movementManager.monitor_obstacles, checkExisting = True )
		scheduleTask( self, self._movementManager.maintain_turret_angle )

	def generateCurve( self ) -> bool:
		pos1 = self.position
		pos2 = self.__curveRootTarget.position
		pos3 = self.__nextTarget.position
		if self._movementManager.generateAndCheckNewCurve( positions = [ pos1, pos2, pos3 ], obstacle = self.__obstacle ):
			targets = self._movementManager.getCurvePoints()
			self.__curveTargets = targets[ ::20 ]
			self.__curveRootTarget = None
			self.__currentTarget = None
			self.bypassTarget = None
			self.removeObstacle()
			return True
		return False

	def generateBypass( self ):
		self.moveTargets.append( self.__currentTarget )
		self.moveTargets.append( self.__bypassTarget )
		self.__bypassTarget = None
		self.__currentTarget = None

	def scheduleBackupTasks( self ):
		scheduleTask( self, self._movementManager.set_velocity_backwards_direction )
		scheduleTask( self, self._movementManager.monitor_obstacles )

	def scheduleCheckObstaclesTasks( self ):
		scheduleTask( self, self._movementManager.track_target_coreBody_angle, checkExisting = True )
		scheduleTask( self, self._movementManager.monitor_obstacles )

	def scheduleObstacleTasks( self ):
		scheduleTask(self, self._movementManager.alternateTargetDetection, checkExisting = True)

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
		self.__detector = Detector (self, physicsWorld, self.__render )
		self._movementManager = MovementManager( self, physicsWorld, self.__render )
		self.__sensors = Senesors( self.coreBodyPath, self._length, self._width, self._height, self.__render )
		self._createStateMachine()
		self._setCorePart()
		self.scheduleVisibility()
		self.selectionPart().model.reparentTo( self.coreBodyPath )

	def clearCurrentTarget( self ):
		if not self.__currentTarget:
			return
		if self.__currentTarget is self.__nextTarget:
			self.__nextTarget = None
		self.__currentTarget = None

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



