from statemachine.state import State
from states.mover.idlestate import IdleState


class StateMachine:
    def __init__( self, entity, initState: State ):
        self.__entity = entity
        self.__currentState: State = initState
        self.__currentState.enter()

    def startMachine( self, task ):
        task.delayTime = 1
        self.__currentState.execute()
        if self.__currentState.done:
            self.changeState( self.__currentState.nextState )
        return task.again

    @property
    def nextState( self ) -> str:
        if self.__currentState.nextState is None:
            self.__currentState.nextState = self.__entity.decide( self.__currentState )
        return self.__currentState.nextState

    def changeState( self, state: str = None ):
        print( f'{ self.__entity.name } sm exit state: { self.__currentState } ')
        self.__currentState.exit()
        self.__currentState = self.__entity.getStateFromEntityPool( state or self.nextState )
        print( f'{ self.__entity.name } sm enter next state: { self.__currentState } ')
        self.__currentState.initialize()
        self.__currentState.enter()
        print( f'{ self.__entity.name } sm execute state: { self.__currentState } ')
