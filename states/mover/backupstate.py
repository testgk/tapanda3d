from typing import TYPE_CHECKING

from entities.locatorMode import LocatorModes
from states.mover.moverstate import MoverState
from states.statenames import States

if TYPE_CHECKING:
	from entities.full.movers.mover import Mover


class BackupState( MoverState ):
	def __init__( self, entity: 'Mover' ):
		super().__init__( entity )

	def enter( self ):
		self.mover.speed = -50
		self.mover.locatorMode = LocatorModes.Edges
		print( f'current target: { self._currentTarget } ' )
		self.mover.scheduleBackupTasks()

	def execute( self ):
		if not self.mover.closeToObstacle():
			self._done = True
			print( f'{ self._entity.name } finished backup' )
			self.nextState = States.OBSTACLE
