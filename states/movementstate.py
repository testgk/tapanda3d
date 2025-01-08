from typing import TYPE_CHECKING
from statemachine.state import State

if TYPE_CHECKING:
	from entities.full.movers.mover import Mover


class MovementState( State ):
	def __init__( self, entity: 'Mover' ):
		super().__init__( entity )
		self.__currentTarget = None

	@property
	def mover( self ) -> 'Mover':
		return self._entity

	def enter( self ):
		self.__currentTarget = self.mover.currentTarget
		self.mover.speed = 50
		self.mover.schedulePointToPointTasks()

	def execute( self ):
		if self.mover.hasObstacles() or self.mover.currentTarget != self.__currentTarget:
			self._done = True
			print( f'{self._entity.name} finished moving' )
			if self.mover.hasObstacles():
				self.nextState = "obstacle"
			else:
				self.nextState = "idle"
		#self.__currentTarget = None
