from typing import TYPE_CHECKING

from entities.locatorMode import LocatorLength, LocatorModes, Locators
from states.moverstate import MoverState
from states.states import States


if TYPE_CHECKING:
    from entities.full.movers.mover import Mover

class ObstacleState( MoverState ):
    def __init__( self, mover: 'Mover' ):
        super().__init__( mover )

    def enter( self ):
        self.mover.stopMovement()
        self.mover.locatorMode = LocatorModes.Edges
        if self.mover.obstacle.detection == Locators.Right:
            self.mover.setDynamicDetector( Locators.Left )
        else:
            self.mover.setDynamicDetector( Locators.Right )
        self.mover.detectorLength = LocatorLength.Medium
        self.mover.scheduleObstacleTasks()

    def execute( self ):
        if self.mover.currentTarget:
            self.mover.removeObstacle()
            self._done = True
            self.nextState = States.IDLE
        if self.mover.curveTarget:
            self._done = True
            self.nextState = States.CURVE
