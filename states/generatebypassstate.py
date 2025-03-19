from typing import TYPE_CHECKING

from entities.locatorMode import LocatorLength
from states.states import States
from states.moverstate import MoverState

if TYPE_CHECKING:
	from entities.full.movers.mover import Mover


class GenerateBypassState( MoverState ):
	def __init__( self, entity: 'Mover' ):
		super().__init__( entity )

	def enter( self ):
		self.mover.detectorLength = LocatorLength.Mininal

	def execute( self ):
		self.mover.removeObstacle()
		self.mover.generateBypass()
		if not self.mover.currentTarget and not self.mover.bypassTarget:
			return self.doneState( States.CAUTIOUS )
