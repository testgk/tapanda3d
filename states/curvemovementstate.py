from typing import TYPE_CHECKING

from entities.locatorMode import LocatorModes, Locators, LocatorLength
from states.movementstate import MovementState
from states.moverstate import MoverState
from states.states import States

if TYPE_CHECKING:
	from entities.full.movers.mover import Mover


class CurveMovementState( MovementState ):
	def __init__( self, entity: 'Mover' ):
		super().__init__( entity )

	def enter( self ):
		self._currentTarget = self.mover.currentTarget
		self.mover.speed = 75
		self.mover.locatorMode = LocatorModes.NONE
		self.mover.setDynamicDetector( Locators.NONE )
		self.mover.detectorLength  = LocatorLength.Short
		self.mover.schedulePointToPointTasks()

	def execute( self ):
		if self.mover.currentTarget != self._currentTarget:
			print( f'mover target: { self.mover.currentTarget }' )
			self._done = True
			self.nextState = States.CURVE_IDLE
