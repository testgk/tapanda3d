from statemachine.state import State

class IdleState( State ):
    def __init__( self, entity ):
        super().__init__( entity )
        self._nextState = "idle"

    def enter( self ):
        self._entity.scheduleIdleMonitoringTask()

    def execute( self ):
        if self._entity.readyToMove:
            self.nextState = "movement"
            self._done = True
