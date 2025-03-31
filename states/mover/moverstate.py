from typing import TYPE_CHECKING

from entities.locatorMode import LocatorModes
from statemachine.state import State
from states.statenames import States

if TYPE_CHECKING:
	from entities.full.movers.mover import Mover


class MoverState( State ):
	def __init__( self, entity: 'Mover' ):
		super().__init__( entity )
		self._currentTarget = None

	@property
	def mover( self ) -> 'Mover':
		return self._entity
