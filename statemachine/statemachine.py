from entities.entity import Entity
from statemachine.state import State
from statemachine.states.processcommandstate import ProcessCommandState


class StateMachine:
    def __init__( self, entity: Entity ):
        self.__entity = entity
        self.__currentState = None

    @property
    def currentState( self ) -> State:
        return self.__currentState

    @property
    def nextState( self ) -> State:
        if self.__currentState.nextState is None:
       #     if self.__entity.pendingCommand():
       #         self.__currentState.nextStat = ProcessCommandState( self.__entity )
            self.__currentState.nextState = self.__currentState.decideNextState()
        return self.__currentState.nextState

    def executeState( self ):
        self.__currentState.execute()

    def previousState( self ) -> State:
        return self.__currentState.previousState

    def changeState( self, state: State ):
        self.__currentState.exit()
        self.__currentState = state or self.nextState
        self.__currentState.enter()
