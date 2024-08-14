from functools import wraps

from statemachine.commands.command import Command
from statemachine.statemachine import StateMachine
from statemachine.states.processcommandstate import ProcessCommandState


def entitypart( tag = None ):
	def decorator( func ):
		@wraps( func )
		def wrapper( * args, ** kwargs ):
			return func( * args, ** kwargs )
		wrapper._is_entity_part = True
		wrapper._tag = tag
		return wrapper
	return decorator


def get_selected_properties( entity, tag = "something" ) :
	selected = { }
	for attr_name in dir( entity ) :
		attr = getattr( entity, attr_name )
		if callable( attr ) and hasattr( attr, "_is_entity_part" ) and attr._is_entity_part :
			if tag is None or attr._tag == tag :
				selected[ attr_name ] = attr()
	return selected


class PartFactory:
	def __init__( self ):
		pass

	def addParts( self, entity ):
		self._parts = get_selected_properties( entity )

	def buildParts( self ):
		pass

	def renderAllParts( self ):
		pass


class Entity:
	def __init__( self ):
		self.__pendingCommand = None
		self._commands = []
		self.name = None
		self._id = None
		self._stationary = None
		self._producer = None
		self._partBuilder = PartFactory()
		self._stateMachine = StateMachine( self )

	def buildAndRender( self ):
		self._createParts()
		self._renderParts()

	def _createParts( self ):
		self._partBuilder.addParts()

	def _renderParts( self ):
		self._partBuilder.renderAllParts()

	def decide( self ):
		currentState = self._stateMachine.currentState
		stateOptions = currentState.possibleNextStates
		return self._decideState( currentState, stateOptions )

	def _decideState( self, currentState, stateOptions ):
		raise NotImplementedError

	def receiveCommand( self, command: Command, serial: bool ):
		if serial:
			self._commands.insert( 0, command )
		else:
			self._commands = [ command ]
			self._stateMachine.changeState( ProcessCommandState( self ) )

	def pendingCommand( self ) -> Command | None:
		if self.__pendingCommand is None:
			self.__pendingCommand = self._commands.pop()
		if self.__pendingCommand.progress == 0:
			return self.__pendingCommand