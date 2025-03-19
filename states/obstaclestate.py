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
        self.mover.speed = 20
        self.mover.stopDistance = True
        self.mover.scheduleObstacleTasks()

    def execute( self ):
        if self.mover.bypassTarget:
            return self.doneState( States.BYPASS )
        if self.mover.curveTarget:
            return self.doneState( States.CURVE )
