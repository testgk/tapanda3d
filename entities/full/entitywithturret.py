from panda3d.bullet import BulletHingeConstraint
from panda3d.core import Vec3

from entities.entity import Entity, entitypart
from entities.modules.chassis import Chassis


class EntityWithTurret:
	def __init__( self, chassis, turret ):
		self._chassis = chassis
		self._turret = turret

	@entitypart
	def turretBase( self ):
		return self._turret.turretBase

	def _connectModules( self, world ):
		pivot_in_hull = Vec3( 0, 0, 1 )
		axis_in_hull = Vec3( 0, 0, 1 )
		pivot_in_turret = Vec3( 0, 0, 0 )
		axis_in_turret = Vec3( 0, 0, 1 )

		hinge = BulletHingeConstraint(
			self._chassis.hull().rigidBody,
			self.turretBase().rigidBody,
			pivot_in_hull, axis_in_hull,
			pivot_in_turret, axis_in_turret,
		)
		hinge.setLimit( 0, 0 )
		hinge.setBreakingThreshold( float( 'inf' ) )
		world.attachConstraint( hinge )