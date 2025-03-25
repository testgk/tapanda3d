from entities.entity import entitypart
from entities.modules.mobilechassis import MobileChassis
from entities.modules.turret import Turret
from entities.full.attacker import Attacker
from entities.full.movers.mover import Mover
from entities.full.entitywithturret import EntityWithTurret


class Tank( Mover, Attacker, EntityWithTurret ):

	def __init__( self, engine, axis: MobileChassis, turret: Turret ):
		super().__init__( chassis = axis, engine = engine )
		EntityWithTurret.__init__( self, axis, turret )

	@entitypart
	def cannon( self ):
		return self._turret.turretCannon

	def _setCoreBodyPath( self ):
		self._coreBodyPath = self._hull

	def _connectModules( self, world ):
		EntityWithTurret._connectModules( self, world, axis = self.hull() )
