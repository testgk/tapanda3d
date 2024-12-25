from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from entities.full.movers.mover import Mover
    from states.movementstate import MovementState

class ObstacleState( MovementState ):
    def __init__( self, mover: 'Mover' ):
        super().__init__( mover )

    def enter( self ):
        self.mover.scheduleObstacleTask()

    def execute( self ):
        if not self.mover.hasObstacles():
            self._done = True
