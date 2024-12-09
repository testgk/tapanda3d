from statemachine.state import State
from states.idlestate import IdleState


class StateMachine:
    def __init__( self, entity ):
        self.__entity = entity
        self.__currentState: State = IdleState( entity )
        self.__currentState.enter()

    def stateMachineMainLoop( self, task ):
        if self.__entity.isSelected():
            print( f"Main loop: current state: { self.__currentState } " )
        if self.__currentState.done:
            self.changeState( self.__currentState.nextState )
        self.__currentState.execute()
        return task.cont

    @property
    def nextState( self ) -> str:
        if self.__currentState.nextState is None:
            self.__currentState.nextState =  self.__entity.decide( self.__currentState )
        return self.__currentState.nextState

    def changeState( self, state: str = None ):
        print( f'{ self.__entity.name } sm exit state: { self.__currentState } ')
        self.__currentState.exit()
        self.__currentState = self.__entity.getStateFromEntityPool( state or self.nextState )
        print( f'{ self.__entity.name } sm enter next state: { self.__currentState } ')
        self.__currentState.initialize()
        self.__currentState.enter()
        print( f'{ self.__entity.name } sm execute state: { self.__currentState } ')
