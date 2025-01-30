from typing import TYPE_CHECKING

from entities.locatorMode import LocatorModes
from statemachine.state import State
from states.movementstate import MovementState
from states.states import States

if TYPE_CHECKING:
	from entities.full.movers.mover import Mover


class CurveState( MovementState ):
	def __init__( self, entity: 'Mover' ):
		super().__init__( entity )
		self._currentTarget = None

	def enter( self ):
		self._currentTarget = self.mover.currentTarget
		self.mover.speed = 75
		self.mover.locatorMode = LocatorModes.All
		self.mover.generateCurve()

	def execute( self ):
		self._done = True
		self.nextState = States.MOVEMENT
