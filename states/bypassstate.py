from typing import TYPE_CHECKING

from entities.locatorMode import LocatorModes
from states.moverstate import MoverState
from states.states import States

if TYPE_CHECKING:
	from entities.full.movers.mover import Mover


class BypassState( MoverState ):
	def __init__( self, entity: 'Mover' ):
		super().__init__( entity )

	def enter( self ):
		self._currentTarget = self.mover.currentTarget
		self.mover.speed = 5
		self.mover.locatorMode = LocatorModes.Edges
		self.mover.schedulePointToPointTasks()

	def execute( self ):
		if self.mover.hasObstacles() or self.mover.currentTarget != self._currentTarget:
			self._done = True
			print( f'{self._entity.name} finished moving' )
			if self.mover.hasObstacles():
				self.nextState = States.OBSTACLE
			else:
				self.nextState = States.IDLE
		elif self.mover.isMidRangeFromObstacle():
			self._done = True
			self.nextState = States.MOVEMENT
