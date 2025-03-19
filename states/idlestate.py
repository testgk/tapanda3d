from typing import TYPE_CHECKING

from statemachine.state import State
from states.states import States

if TYPE_CHECKING:
    from entities.full.movers.mover import Mover

class IdleState( State ):
    def __init__( self, entity: 'Mover' ):
        super().__init__( entity )
        self._nextState = "idle"

    @property
    def mover( self ) -> 'Mover':
        return self._entity

    def enter( self ):
        self._entity.scheduleTargetMonitoringTask()

    def execute( self ):
        if self.mover.currentTarget:
            return self.doneState( States.CHECK_OBSTACLE )
        #if self.mover.bypassTarget:
        #    self.nextState = States.MOVEMENT
        #    self._done = True
