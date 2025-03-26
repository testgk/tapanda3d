from typing import TYPE_CHECKING

from entities.locatorMode import LocatorModes, Locators, LocatorLength
from states.mover.movementstate import MovementState
from states.states import States

if TYPE_CHECKING:
	from entities.full.movers.mover import Mover


class CurveMovementState( MovementState ):
	def __init__( self, entity: 'Mover' ):
		super().__init__( entity )

	def enter( self ):
		self._currentTarget = self.mover.currentTarget
		self.mover.speed = 75
		self.mover.locatorMode = LocatorModes.Edges
		self.mover.detectors.setDynamicDetector( Locators.Full )
		self.mover.detectorLength = LocatorLength.Medium
		self.mover.stopDistance = False
		self.mover.schedulePointToPointTasks()

	def execute( self ):
		if not self.mover.insideCurve:
			return self.doneState( States.IDLE )
		if self.mover.currentTarget != self._currentTarget:
			self.mover.terminateCurve()
			return self.doneState( States.CURVE_IDLE )
