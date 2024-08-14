from entities.partfactory import PartFactory
from entities.commandmanager import CommandManager
from statemachine.commands.command import Command
from statemachine.statemachine import StateMachine


def entitypart( func ):
    func._is_entitypart = True  # Mark the function or property with an attribute
    return func

def entityplatform( func ):
    func._is_entitypart = True  # Mark the function or property with an attribute
    return func

class Entity:
    def __init__( self ):
        self.__pendingCommand = None
        self._commands = []
        self.name = None
        self._id = None
        self._stationary = None
        self._producer = None
        self._partBuilder = PartFactory( self )
        self._stateMachine = StateMachine( self )
        self._commandManager = CommandManager()

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
        self._commandManager.receiveCommand( command )

    def pendingCommand( self ) -> Command | None:
       return self._commandManager.pendingCommand()