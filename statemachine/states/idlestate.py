from entities.entity import Entity
from statemachine.state import State
from statemachine.statemachine import StateMachine
from statemachine.states.processcommandstate import ProcessCommandState


class IdleState( State ):
    def __init__( self, entity: Entity ):
        super().__init__( entity )

    @property
    def nextState( self ):
        return ProcessCommandState()


    def enter( self ):
        pass

    def exit( self ):
        pass

    def execute( self ):
        pass