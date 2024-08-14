from statemachine.commands.command import Command
from statemachine.state import State
from statemachine.statemachine import StateMachine
from statemachine.states.processcommandstate import ProcessCommandState


class PartBuilder:
    def addPart( self, part ):
        pass

    def addParts( self, _parts ):
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
        self._parts = None
        self._partBuilder = PartBuilder()
        self._stateMachine = StateMachine( self )

    def build( self ):
        self._setParts()
        self._createParts()

    def _setParts( self ):
        raise NotImplementedError

    def _createParts( self ):
        self._partBuilder.addParts( self._parts )
        self._partBuilder.renderAllParts()

    def decide( self ) -> State:
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