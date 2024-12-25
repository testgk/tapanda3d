from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import Vec3

from entities.modules.chassis import Chassis
from entities.parts.engine import Engine
from entities.entity import Entity, entitypart, entitymodule
from entities.parts.part import Part
from movement.movementmgr import MovementManager
from selectionitem import SelectionItem
from selectionmodes import SelectionModes
from statemachine.state import State
from states.idlestate import IdleState
from states.movementstate import MovementState


class Mover( Entity ):

	def __init__( self, engine, chassis: Chassis ):
		super().__init__()
		self._movementManager = None
		self.__hpr = None
		self.regularSpeed = 100
		self.readyToMove = False
		self._chassis = chassis
		self._currentPosition = None
		self._engine = engine
		self._mobility = chassis.mobility()
		self._hull = chassis.hull()
		self._corePart = self.mobility()
		self._isMover = True
		self._currentTarget = None
		self.__terrainSize = None

	@property
	def currentTarget( self ) -> SelectionItem:
		return self._currentTarget

	@property
	def hpr( self ) -> Vec3:
		if self.coreBodyPath:
			return Vec3( self.coreBodyPath  )

	def monitorIdleState( self, task ):
		if self.selectTargets.empty():
			return task.cont
		print( f'{self.name} moving p2p to {self.selectTargets}' )
		self.readyToMove = True
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
		}

	def scheduleIdleMonitoringTask( self ):
		self.scheduleTask( self.monitorIdleState, "monitoring command" )

	@property
	def terrainSize( self ):
		return self.__terrainSize

	@terrainSize.setter
	def terrainSize( self, terrainSize ):
		self.__terrainSize = terrainSize

	def schedulePointToPointTask( self ):
		self._currentTarget = self.selectTargets.get()
		position = self._currentTarget.position
		self.scheduleTask(
				self._movementManager.set_velocity_toward_point_with_stop,
				f"{self.name}_move_p2p",
				extraArgs = [ position ],
				appendTask = True
		)
		self.scheduleTask(
				self._movementManager.track_target_angle,
				f"{self.name}_monitor_angle",
				extraArgs = [ position ],
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
				extraArgs = [ position ],
				appendTask = True
		)
		self.scheduleTask(
				self._movementManager.maintain_turret_angle,
				f"{self.name}_maintain_turret_angle",
				extraArgs = [ position ],
				appendTask = True
		)

	def handleObstacleTask( self ):
		position = self._currentTarget.position
		self.scheduleTask(
				self._movementManager.handleObstacleTask,
				f"{self.name}_move_p2p",
				extraArgs = [ position ],
				appendTask = True
		)


	def scheduleObstacleTask( self ):
		pass

	def finishedMovement( self ):
		if taskMgr.hasTaskNamed( f"{self.name}_move_p2p" ):
			return False
		self.readyToMove = False
		return True

	def hasObstacles( self ) -> bool:
		return self._movementManager.anyObstacles

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
		self.createStateMachine()
		self.initMovementManager( physicsWorld )

