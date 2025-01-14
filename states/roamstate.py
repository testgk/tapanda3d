from typing import TYPE_CHECKING

from entities.locatorMode import LocatorModes
from statemachine.state import State
from states.states import States
from states.movementstate import MovementState

if TYPE_CHECKING:
	from entities.full.movers.mover import Mover


class RoamState( MovementState ):
	def __init__( self, entity: 'Mover' ):
		super().__init__( entity )
		self._currentTarget = None

	def enter( self ):
		self._currentTarget = self.mover.currentTarget
		self.mover.speed = 75
		self.mover.locatorMode = LocatorModes.DynamicOnly
		self.mover.schedulePointToPointTasks()

	def execute( self ):
		if self.mover.hasObstacles() or self.mover.currentTarget != self._currentTarget:
			self._done = True
			print( f'{self._entity.name} finished moving' )
			if self.mover.hasObstacles():
				self.nextState = States.MOVEMENT
			else:
				self.nextState = States.IDLE
		#self.__currentTarget = None
