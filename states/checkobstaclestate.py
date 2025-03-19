from typing import TYPE_CHECKING

from entities.locatorMode import LocatorModes
from statemachine.state import State
from states.movementstate import MovementState
from states.states import States

if TYPE_CHECKING:
	from entities.full.movers.mover import Mover


class CheckObstacle( MovementState ):
	def __init__( self, entity: 'Mover' ):
		super().__init__( entity )

	def enter( self ):
		self.mover.locatorMode = LocatorModes.TargetOnly
		self.mover.scheduleCheckObstaclesTasks()

	def execute( self ):
		if self.mover.hasObstacles():
			return self.doneState( States.OBSTACLE )
		elif self.mover.aligned:
			return self.doneState( States.MOVEMENT )
