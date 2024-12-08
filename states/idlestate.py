from statemachine.state import State
from states.movementstate import MovementState

class IdleState( State ):
    def __init__( self, entity ):
        super().__init__( entity )
        self._nextState = self

    def enter( self ):
        self._entity.scheduleTask( self._entity.monitorIdleState, "monitoring command" )

    def execute( self ):
        if self._entity.readyToMove:
            self.nextState = MovementState( self._entity )
            self._done = True

    def exit( self ):
        pass
