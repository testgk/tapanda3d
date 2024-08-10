from entities.entity import Entity
from statemachine.state import State
from statemachine.statemachine import StateMachine


class IdleState( State ):
    def __init__( self, entity: Entity ):
        super().__init__( entity )

    def enter( self ):
        super()._reportState( "enter" )


    def exit( self ):
        pass


    def execute( self ):
