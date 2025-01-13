from typing import TYPE_CHECKING

from entities.locatorMode import LocatorModes
from statemachine.state import State
from states.movementstate import MovementState

if TYPE_CHECKING:
	from entities.full.movers.mover import Mover


class BypassState( MovementState ):
	def __init__( self, entity: 'Mover' ):
		super().__init__( entity )

	def enter( self ):
		self._currentTarget = self.mover.currentTarget
		self.mover.speed = 10
		self.mover.locatorMode = LocatorModes.Edges
		self.mover.schedulePointToPointTasks()

	def execute( self ):
		if self.mover.hasObstacles() or self.mover.currentTarget != self._currentTarget:
			self._done = True
			print( f'{self._entity.name} finished moving' )
			if self.mover.hasObstacles():
				self.nextState = "obstacle"
			else:
				self.nextState = "idle"
		elif self.mover.isMidRangeFromObstacle():
			self._done = True
			self.nextState = "movement"
