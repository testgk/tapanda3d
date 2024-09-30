from sys import modules

from panda3d.core import NodePath

from entities.partfactory import PartFactory
from entities.commandmanager import CommandManager
from statemachine.commands.command import Command
from statemachine.statemachine import StateMachine


def entitypart( func ):
	func._is_entitypart = True  # Mark the function or property with an attribute
	return func


def entitymodule( func ):
	func._is_entitymodule = True  # Mark the function or property with an attribute
	return func


def nonrenderedpart( func ):
	func._is_nonrenderd = True  # Mark the function or property with an attribute
	return func


class Entity:
	def __init__( self ):
		self.__pendingCommand = None
		self._commands = [ ]
		self.name = None
		self._id = None
		self.__models = [ ]
		self._partBuilder = PartFactory( self )
		self._stateMachine = StateMachine( self )
		self._commandManager = CommandManager()
		self.__collisionSystems = [ ]
		self.__rigidBodyNode = None

	@property
	def models( self ) -> list[ NodePath ]:
		return self.__models

	@property
	def collisionSystems( self ):
		return self.__collisionSystems

	@property
	def rigidBodyNode( self ):
		return self.__rigidBodyNode

	def buildModels( self, loader ):
		self._createParts()
		self._buildParts( loader )
		#self._createCollisionSystems()
		self._createRigidBodies()

	def _createParts( self ):
		self._partBuilder.addParts()

	def _buildParts( self, loader ):
		self.__models = self._partBuilder.buildAllParts( loader )

	def _createCollisionSystems( self ):
		self.__collisionSystems = self._partBuilder.createCollisionSystem( self.__models )
		for collisionNode in self.__collisionSystems:
			collisionNode.setPythonTag( 'collision_target', self )

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

	def _createRigidBodies( self ):
		self.__rigidBodyNode = self._partBuilder.createRigidBodies( self.__models )
