from typing import TYPE_CHECKING

from entities.locatorMode import LocatorLength, LocatorModes, Locators
from states.mover.moverstate import MoverState
from states.statenames import StateNames

if TYPE_CHECKING:
	from entities.full.movers.mover import Mover


class MovementState( MoverState ):
	def __init__( self, entity: 'Mover' ):
		super().__init__( entity )

	def enter( self ):
		self._currentTarget = self.mover.currentTarget
		self.mover.speed = 75
		self.mover.locatorMode = LocatorModes.DynamicOnly
		self.mover.stopAtDistance = True
		self.mover.detectorLength = LocatorLength.Medium
		self.mover.sensors.setDynamicDetector( Locators.Full )
		self.mover.schedulePointToPointTasks()

	def execute( self ):
		if self.mover.hasObstacles():
			return self.doneState(StateNames.OBSTACLE)
		if self.mover.currentTarget is None:
			return self.doneState(StateNames.IDLE)
		if self.mover.currentTarget != self._currentTarget:
			return self.doneState(StateNames.MOVEMENT)
		return None
