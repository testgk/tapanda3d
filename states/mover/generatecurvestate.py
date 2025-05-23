from typing import TYPE_CHECKING

from states.statenames import States
from states.mover.moverstate import MoverState
from entities.locatorMode import LocatorModes, Locators

if TYPE_CHECKING:
	from entities.full.movers.mover import Mover


class GenerateCurveState( MoverState ):
	def __init__( self, entity: 'Mover' ):
		super().__init__( entity )

	def enter( self ):
		self.mover.speed = 0
		self.mover.locatorMode = LocatorModes.All
		#self.mover.bypassTarget = None

	def execute( self ):
		self.mover.generateCurve()
		if self.mover.curveRootTarget:
			return self.doneState( States.BYPASS )

		return self.doneState( States.CURVE_IDLE )
