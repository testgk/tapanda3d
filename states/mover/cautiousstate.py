from typing import TYPE_CHECKING

from entities.locatorMode import LocatorLength, LocatorModes
from states.mover.moverstate import MoverState
from states.states import States

if TYPE_CHECKING:
	from entities.full.movers.mover import Mover


class CautiousState( MoverState ):
	def __init__( self, entity: 'Mover' ):
		super().__init__( entity )

	def enter( self ):
		self._currentTarget = self.mover.currentTarget
		self.mover.speed = 25
		self.mover.locatorMode = LocatorModes.TargetOnly
		self.mover.detectorLength = LocatorLength.Medium
		self.mover.schedulePointToPointTasks()
		self.mover.scheduleTargetMonitoringTask()

	def execute( self ):
		if not self.mover.aligned:
			self.mover.locatorMode = LocatorModes.TargetOnly
		else:
			self.mover.locatorMode = LocatorModes.Edges

		if self.mover.currentTarget != self._currentTarget:
			return self.doneState( States.IDLE )
