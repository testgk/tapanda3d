from typing import TYPE_CHECKING

from entities.locatorMode import LocatorModes, Locators, LocatorLength
from states.mover.movementstate import MovementState
from states.statenames import StateNames

if TYPE_CHECKING:
	from entities.full.movers.mover import Mover


class CurveMovementState( MovementState ):
	def __init__( self, entity: 'Mover' ):
		super().__init__( entity )

	def enter( self ):
		self._currentTarget = self.mover.currentTarget
		self.mover.speed = 75
		self.mover.locatorMode = LocatorModes.TargetOnly
		self.mover.sensors.setDynamicDetector( Locators.Full )
		self.mover.detectorLength = LocatorLength.Medium
		self.mover.stopAtDistance = False
		self.mover.schedulePointToPointTasks()

	def execute( self ) ->None:
		if not self.mover.insideCurve:
			self.mover.terminateCurve()
			return self.doneState( StateNames.IDLE )
		if self.mover.currentTarget != self._currentTarget:
			return self.doneState( StateNames.CURVE_IDLE )
		return None
