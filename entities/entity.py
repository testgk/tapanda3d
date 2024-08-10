from statemachine.state import State
from statemachine.statemachine import StateMachine


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
        self.commands = None
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

    def pendingCommand( self ) -> str:
        self.__pendingCommand = self.commands.pop()
        return self.__pendingCommand