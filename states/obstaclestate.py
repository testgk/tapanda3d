from typing import TYPE_CHECKING

from states.movementstate import MovementState


if TYPE_CHECKING:
    from entities.full.movers.mover import Mover

class ObstacleState( MovementState ):
    def __init__( self, mover: 'Mover' ):
        super().__init__( mover )

    def enter( self ):
        self.mover.scheduleObstacleTasks()

    def execute( self ):
        if not self.mover.hasObstacles():
            self._done = True
            self.nextState = "bypass"
