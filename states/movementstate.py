from typing import TYPE_CHECKING
from statemachine.state import State

if TYPE_CHECKING:
	from entities.full.movers.mover import Mover


class MovementState( State ):
	def __init__( self, entity: 'Mover' ):
		super().__init__( entity )
		self._currentTarget = None

	@property
	def mover( self ) -> 'Mover':
		return self._entity

	def enter( self ):
		self._currentTarget = self.mover.currentTarget
		self.mover.speed = 75
		self.mover.schedulePointToPointTasks()

	def execute( self ):
		if self.mover.hasObstacles() or self.mover.currentTarget != self._currentTarget:
			self._done = True
			print( f'{self._entity.name} finished moving' )
			if self.mover.hasObstacles():
				self.nextState = "obstacle"
			else:
				self.nextState = "idle"
		#self.__currentTarget = None
