from typing import TYPE_CHECKING
from statemachine.state import State

if TYPE_CHECKING:
	from entities.full.movers.mover import Mover


class MovementState( State ):

	def __init__( self, entity: 'Mover' ):
		super().__init__( entity )

	@property
	def mover( self ) -> 'Mover':
		return self._entity

	def enter( self ):
		self.mover.schedulePointToPointTask()

	def execute( self ):
		if self.mover.finishedMovement():
			self._done = True
			print( f'{self._entity.name} finished moving' )
			if self.mover.hasObstacles():
				self.nextState = "obstacle"
			else:
				self.mover.currentTarget.clearSelection()
				self.mover.currentTarget = None
