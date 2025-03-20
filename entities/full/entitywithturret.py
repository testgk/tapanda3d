from entities.entity import Entity, entitypart
from entities.modules.chassis import Chassis


class EntityWithTurret:
	def __init__( self, turret ):
		self._turret = turret

	@entitypart
	def turretBase( self ):
		return self._turret.turretBase

	@entitypart
	def cannon( self ):
		return self._turret.turretCannon