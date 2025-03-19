from typing import TYPE_CHECKING

from statemachine.state import State
from states.idlestate import IdleState
from states.states import States

if TYPE_CHECKING:
    from entities.full.movers.mover import Mover

class CurveIdleState( IdleState ):
    def __init__( self, entity: 'Mover' ):
        super().__init__( entity )

    def enter( self ):
        self.mover.scheduleCurveMovementMonitoringTaskTask()

    def execute( self ):
        if self.mover.currentTarget:
            if self.mover.insideCurve:
                self.nextState = States.CURVE_MOVEMENT
            else:
                self.nextState = States.IDLE
            self._done = True
