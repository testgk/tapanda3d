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
		self.mover.generateCurve()
		#self.mover.obstacle.clearSelection()
		#self.mover.obstacle = None

	def execute( self ):
		return
		self._done = True
		self.nextState = States.MOVEMENT
