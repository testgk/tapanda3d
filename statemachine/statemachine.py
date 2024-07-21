from statemachine.state import State


class StateMachine:
    def __init__( self, entity ):
        self.__entity = entity
        self.__currentState = None

    @property
    def currentState( self ):
        return self.__currentState

    def nextState(self):
        return self.__currentState.nextState

    def executeState( self ):
        self.__currentState.execute()

    def previousState(self):
        return self.__currentState.previousState

    def changeState(self, newState: State ):
        self.__currentState.exit()
        self.__currentState = newState
        self.__currentState.enter()
