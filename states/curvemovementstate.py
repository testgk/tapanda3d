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
		self.mover.locatorMode = LocatorModes.Edges
		self.mover.setDynamicDetector( Locators.Full )
		self.mover.detectorLength = LocatorLength.Medium
		self.mover.stopDistance = False
		self.mover.schedulePointToPointTasks()

	def execute( self ):
		if self.mover.hasObstacles():
			self.nextState = States.OBSTACLE
			self._done = True
			return
		if self.mover.currentTarget != self._currentTarget:
			print( f'mover target: { self.mover.currentTarget }' )
			self._done = True
			self.nextState = States.CURVE_IDLE
