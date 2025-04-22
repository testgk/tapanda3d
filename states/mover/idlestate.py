from entities.locatorMode import LocatorLength, LocatorModes, Locators
from states.statenames import States
from statemachine.state import State

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from entities.entity import Entity

class IdleState( State ):
    def __init__( self, entity: 'Entity' ) -> None:
        super().__init__( entity )
        self._nextState = "idle"

    def enter( self ):
        self._entity.locatorMode = LocatorModes.DynamicOnly
        self._entity.detectorLength = LocatorLength.Medium
        self._entity.sensors.setDynamicDetector( Locators.Full )
        self._entity.scheduleTargetMonitoringTask()
        self._entity.scheduleMaintainTurretAngleTask()

    def execute( self ):
        if self._entity.currentTarget:
            return self.doneState( States.CHECK_OBSTACLE )
        return None
