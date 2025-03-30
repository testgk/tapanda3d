from panda3d.bullet import BulletHingeConstraint
from panda3d.core import Vec3

from entities.entity import entitypart
from scheduletask import scheduleTask


class EntityWithTurret:
	def __init__( self, axis, turret, movementMgr ):
		self.__aligned = False
		self._axis = axis
		self._turret = turret
		self.__movementMgr = movementMgr

	@entitypart
	def turretBase( self ):
		if self._turret:
			return self._turret.turretBase

	@property
	def aligned( self ):
		return self.__aligned

	@aligned.setter
	def aligned( self, value ):
		self.__aligned = value

	def _connectModules( self, world, axis ):
		pivot_in_hull = Vec3( 0, 0, 1 )
		axis_in_hull = Vec3( 0, 0, 1 )
		pivot_in_turret = Vec3( 0, 0, 0 )
		axis_in_turret = Vec3( 0, 0, 1 )

		hinge = BulletHingeConstraint( axis.rigidBody,
							self.turretBase().rigidBody,
							pivot_in_hull, axis_in_hull,
							pivot_in_turret, axis_in_turret,
						)
		hinge.setLimit( 0, 0 )
		hinge.setBreakingThreshold( float( 'inf' ) )
		world.attachConstraint( hinge )

	def schedulePointToPointTasks( self ):
		scheduleTask( self._turret.name, self.__movementMgr.maintain_turret_angle )
