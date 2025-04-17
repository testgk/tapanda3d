from abc import ABC

from entities.entity import entitypart
from entities.modules.turret import Turret
from entities.full.attacker import Attacker
from entities.full.movers.mover import Mover
from entities.entitywithturret import EntityWithTurret
from entities.modules.mobilechassis import MobileChassis


class Tank( Mover, Attacker, EntityWithTurret, ABC ):

	def __init__( self, engine, axis: MobileChassis, turret: Turret ):
		super().__init__( chassis = axis, engine = engine )
		EntityWithTurret.__init__( self, self.hull() , turret )

	@entitypart
	def cannon( self ):
		return self._turret.turretCannon

	def _setCorePart( self ):
		self._coreBodyPath = self._turret

	def _connectModules( self, world ):
		EntityWithTurret._connectTurret( self, world, axis = self.hull() )
