from panda3d.bullet import BulletHingeConstraint
from panda3d.core import Vec3

from entities.entity import entitypart
from scheduletask import scheduleTask


class EntityWithTurret:
	def __init__( self, axis, turret ):
		self.__world = None
		self.__aligned = False
		self._axis = axis
		self._turret = turret
		self._movementManager = None

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

	def _connectTurret( self, world, axis ):
		if not self.__world:
			self.__world = world
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

	def keepTurret( self, task ):
		task.delayTime = 1.0
		self._connectTurret( self.__world, axis = self._axis )
		return task.again

	def scheduleMaintainTurretAngleTask( self ):
		scheduleTask( self, self._movementManager.track_target_coreBody_angle )
		scheduleTask( self, self.keepTurret )
