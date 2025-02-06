from typing import TYPE_CHECKING

from states.states import States
from states.moverstate import MoverState
from entities.locatorMode import LocatorModes

if TYPE_CHECKING:
	from entities.full.movers.mover import Mover


class CurveState( MoverState ):
	def __init__( self, entity: 'Mover' ):
		super().__init__( entity )

	def enter( self ):
		self.mover.speed = 0
		self.mover.locatorMode = LocatorModes.All
		self.mover.terminateCurve()
		self.mover.bpTarget = None

	def execute( self ):
		if self.mover.generateCurve():
			#self.mover.clearCurrentTarget()
			self._done = True
			self.nextState = States.MOVEMENT
		else:
			self.mover.terminateCurve()
			self._done = False
