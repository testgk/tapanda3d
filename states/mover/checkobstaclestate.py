from typing import TYPE_CHECKING

from states.statenames import StateNames
from entities.locatorMode import LocatorModes
from states.mover.movementstate import MovementState

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
			return self.doneState(StateNames.OBSTACLE)
		elif self.mover.aligned:
			return self.doneState(StateNames.MOVEMENT)
