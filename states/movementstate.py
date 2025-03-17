from typing import TYPE_CHECKING

from entities.locatorMode import LocatorLength, LocatorModes, Locators
from states.moverstate import MoverState
from states.states import States

if TYPE_CHECKING:
	from entities.full.movers.mover import Mover


class MovementState( MoverState ):
	def __init__( self, entity: 'Mover' ):
		super().__init__( entity )
		self._currentTarget = None

	def enter( self ):
		self._currentTarget = self.mover.currentTarget
		self.mover.speed = 75
		self.mover.locatorMode = LocatorModes.Edges
		self.mover.stopDistance = True
		self.mover.detectorLength = LocatorLength.Medium
		self.mover.setDynamicDetector( Locators.Full )
		self.mover.schedulePointToPointTasks()

	def execute( self ):
		if self.mover.hasObstacles() or self.mover.currentTarget != self._currentTarget:
			print( f'mover target: { self.mover.currentTarget }' )
			self._done = True
			print( f'{ self._entity.name } finished moving' )
			if self.mover.hasObstacles():
				print( f'obstacle detected' )
				self.nextState = States.OBSTACLE
			else:
				if self.mover.currentTarget is None:
					print( f'no more targets' )
					self.nextState = States.IDLE
				else:
					self.nextState = States.BYPASS
