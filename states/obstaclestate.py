from typing import TYPE_CHECKING
from statemachine.state import State

if TYPE_CHECKING:
    from entities.full.movers.mover import Mover
    from states.movementstate import MovementState

class ObstacleState( MovementState ):
    def __init__( self, mover: 'Mover' ):
        super().__init__( mover )

    def enter( self ):
        self.mover.scheduleObstacleTask()

    def execute( self ):
        if not self.mover.obstacle():
            self._done = True
