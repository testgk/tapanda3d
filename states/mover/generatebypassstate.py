from typing import TYPE_CHECKING

from entities.locatorMode import LocatorLength
from states.statenames import StateNames
from states.mover.moverstate import MoverState

if TYPE_CHECKING:
	from entities.full.movers.mover import Mover


class GenerateBypassState( MoverState ):
	def __init__( self, entity: 'Mover' ):
		super().__init__( entity )

	def enter( self ) -> None:
		self.mover.detectorLength = LocatorLength.Mininal

	def execute( self ) -> None:
		self.mover.removeObstacle()
		self.mover.generateBypass()
		if not self.mover.currentTarget and not self.mover.bypassTarget:
			return self.doneState( StateNames.CAUTIOUS )
		return None
