from sys import modules

from panda3d.bullet import BulletRigidBodyNode
from panda3d.core import NodePath

from entities.partfactory import PartFactory
from entities.commandmanager import CommandManager
from enums.colors import Color
from selectionitem import SelectionItem
from selectionmodes import SelectionModes
from statemachine.commands.command import Command
from statemachine.statemachine import StateMachine


def entitypart( func ):
	func._is_entitypart = True
	return func


def entitymodule( func ):
	func._is_entitymodule = True
	return func


def nonrenderedpart( func ):
	func._is_nonrenderd = True
	return func


class Entity( SelectionItem ):
	def __init__( self ):
		super().__init__()
		self._coreRigidBody = None
		self._coreRigidGroup = None
		self.__pendingCommand = None
		self._commands = [ ]
		self.name = None
		self._id = None
		self.__models = [ ]
		self._partBuilder = PartFactory( self )
		self._stateMachine = StateMachine( self )
		self._commandManager = CommandManager()
		self.__collisionSystems = [ ]
		self.__rigidBodies = None
		self._corePart = None
		self._coreBody = None

	@property
	def models( self ) -> list[ NodePath ]:
		return self.__models

	@property
	def collisionSystems( self ):
		return self.__collisionSystems

	@property
	def rigidBodyNodes( self ) -> dict:
		return self.__rigidBodies

	@property
	def coreBody( self ) -> NodePath:
		return self._coreBody

	@property
	def coreRigidBody( self ) -> BulletRigidBodyNode:
		return self._coreRigidBody

	def setCoreBody( self, coreBody, bulletCoreBody ):
		self._coreBody = coreBody
		self._coreRigidBody = bulletCoreBody

	def buildModels( self, loader ):
		self._partBuilder.build( loader )
		self.__models = self._partBuilder.models
		self.__collisionSystems = self._partBuilder.collisionSystems
		for collisionNode in self.__collisionSystems:
			collisionNode.setPythonTag( 'collision_target', self )
		self.__rigidBodies = self._partBuilder.rigidBodies

	def isRigidGroup( self, rigidGroup ) -> bool:
		return self._corePart.rigidGroup == rigidGroup

	def decide( self ):
		currentState = self._stateMachine.currentState
		stateOptions = currentState.possibleNextStates
		return self._decideState( currentState, stateOptions )

	def _decideState( self, currentState, stateOptions ):
		raise NotImplementedError

	def receiveCommand( self, command: Command, serial: bool ):
		self._commandManager.receiveCommand( command )

	def pendingCommand( self ) -> Command | None:
		return self._commandManager.pendingCommand()

	def handleSelection( self, mode: SelectionModes ):
		if self.isSelected( mode ):
			return

		self._selectionMode = mode
		if mode == SelectionModes.P2P:
			for model in self.__models:
				model.setColor( Color.GREEN.value )
		for system in self.__collisionSystems:
			system.show()

	def clearSelection( self ):
		self._selectionMode = SelectionModes.NONE
		for model in self.__models:
			part = model.node().getPythonTag( 'model_part' )
			model.setColor( part.color )
		for system in self.__collisionSystems:
			system.hide()
