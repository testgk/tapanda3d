from typing import TYPE_CHECKING

from statemachine.state import State
from states.movementstate import MovementState

if TYPE_CHECKING:
	from entities.full.attacker import Attacker


class StuckState( State ):
	def __init__( self, entity: 'Attacker' ):
		super().__init__( entity )

	@property
	def attacker( self ) -> 'Attacker':
		return self._entity

	def enter( self ):
		self._currentTarget = self.attacker.attackTarget
		self.attacker.scheduleAttackingTasks()

	def execute( self ):
		pass
