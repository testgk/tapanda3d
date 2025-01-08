from typing import TYPE_CHECKING
from statemachine.state import State
from states.movementstate import MovementState

if TYPE_CHECKING:
	from entities.full.movers.mover import Mover


class BypassState( MovementState ):
	def __init__( self, entity: 'Mover' ):
		super().__init__( entity )

	def enter( self ):
		self.mover.speed = 10
		self.mover.schedulePointToPointTasks()

	def execute( self ):
		if self.mover.bpTarget is not None:
			if self.mover.isMidRangeFromObstacle() or self.mover.isTargetVisible():
				self._done = True
				self.nextState = "movement"

