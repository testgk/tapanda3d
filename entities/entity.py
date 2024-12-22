import random
from collections import defaultdict

from direct.task.Task import TaskManager
from panda3d.bullet import BulletRigidBodyNode
from panda3d.core import NodePath

from entities.partfactory import PartFactory
from entities.commandmanager import CommandManager
from selectionitem import SelectionItem
from selectionmodes import SelectionModes
from statemachine.commands.command import Command
from statemachine.state import State
from statemachine.statemachine import StateMachine
from states.idlestate import IdleState


def entitypart( func ):
	func._is_entitypart = True
	return func


def entitymodule( func ):
	func._is_entitymodule = True
	return func


class Entity( SelectionItem ):
	def __init__( self ):
		super().__init__()
		self._statesPool = None
		self._taskMgr = None
		self._stateMachine = None
		self.__pendingCommand = None
		self._commands = [ ]
		self.name = f'{ self.__class__.__name__}_{ random.randint(1, 1000 ) }'
		self._id = None
		self.__models = [ ]
		self._partBuilder = PartFactory( self )
		self._commandManager = CommandManager()
		self.__collisionSystems = [ ]
		self.__rigidBodies = None
		self._corePart = None
		self._coreBodyPath = None
		self.initStatesPool()

	@property
	def collisionSystems( self ):
		return self.__collisionSystems

	@property
	def rigidBodyNodes( self ) -> dict:
		return self.__rigidBodies

	@property
	def coreBodyPath( self ) -> NodePath:
		return self._corePart.rigidBodyPath

	@property
	def coreRigidBody( self ) -> BulletRigidBodyNode:
		return self._corePart.rigidBody

	@property
	def selectBox( self ):
		try:
			return self.__collisionSystems[ 0 ]
		except IndexError:
			return None

	def createStateMachine( self, taskManager: TaskManager ):
		self._taskMgr = taskManager
		self._stateMachine = StateMachine( self )
		self.scheduleTask( self._stateMachine.stateMachineMainLoop, f"{ self.name}_state_machine_loop", appendTask = True  )

	def setCoreBody( self, coreBodyPath: NodePath, bulletCoreBody: BulletRigidBodyNode ):
		self._coreBodyPath = coreBodyPath
		self._coreRigidBody = bulletCoreBody

	@property
	def position( self ):
		if self.coreBodyPath:
			return self.coreBodyPath.get_pos()

	@property
	def models( self ):
		return self._partBuilder.models

	def buildModels( self, loader ):
		self._partBuilder.build( loader )
		self.__models = self._partBuilder.models
		self.__collisionSystems = self._partBuilder.collisionSystems
		for collisionNode in self.__collisionSystems:
			collisionNode.setPythonTag( 'collision_target', self )
		self.__rigidBodies = self._partBuilder.rigidBodies

	def connectModules( self, world ):
		raise NotImplementedError

	def isCoreBodyRigidGroup( self, rigidGroup: str ) -> bool:
		return self._corePart.rigidGroup == rigidGroup

	def decide( self, currentState: State ) -> str:
		raise NotImplementedError

	def getStateFromEntityPool( self, stateName: str ):
		return self._statesPool[ stateName ]

	def receiveCommand( self, command: Command, serial: bool ):
		self._commandManager.receiveCommand( command )

	def pendingCommand( self ) -> Command | None:
		return self._commandManager.pendingCommand()

	def scheduleTask( self, method, name: str, extraArgs: list = None, appendTask = True ):
		self._taskMgr.add( method, name = name, extraArgs = extraArgs, appendTask = appendTask )

	def setDamping( self ):
		self.coreRigidBody.set_linear_damping( 0 )
		self.coreRigidBody.set_angular_damping( 0 )

	def isSelected( self, mode: SelectionModes = None ) -> bool:
		return self._selectionMode != SelectionModes.NONE

	def handleSelection( self, mode: SelectionModes ):
		if self.isSelected( mode ):
			self.clearSelection()
		self._selectionMode = SelectionModes.P2P
		self.selectBox.show()

	def clearSelection( self ):
		self._selectionMode = SelectionModes.NONE
		for model in self.__models:
			part = model.node().getPythonTag( 'model_part' )
			model.setColor( part.color )
		for system in self.__collisionSystems:
			system.hide()

	def handleSelectItem( self, item: 'SelectionItem' ) -> SelectionItem | None:
		if item == self:
			self.clearSelection()
		#if item.isMover:
		#	self.clearSelection()
			#while not self._selectTargets.empty():
			#	target = self._selectTargets.get()
			#	target.clearSelection()
			if item != self:
				item.handleSelection( SelectionModes.P2P )
				return item
		if item.isTerrain:
			self._selectTargets.put( item )
			item.handleSelection( SelectionModes.P2P )
			return self
		return None

	def initStatesPool( self ):
		self._statesPool = {
			"idle" : IdleState,
		}
