from panda3d.bullet import BulletHingeConstraint
from panda3d.core import Vec3

from entities.entity import entitypart
from entities.full.movers.mover import Mover
from entities.modules.chassis import Chassis
from entities.modules.turret import Turret


class Tank( Mover ):
    def __init__( self, engine, chassis: Chassis, turret: Turret ):
        super().__init__( chassis = chassis, engine = engine )
        self.__turret = turret

    @entitypart
    def turretBase( self ):
        return self.__turret.turretBase

    @entitypart
    def cannon( self ):
        return self.__turret.turretCannon

    def _maintainTurretAngle( self, target ):
        self.scheduleTask(
            self._movementManager.maintain_turret_angle,
            f"{ self.name }_maintain_turret_angle",
            extraArgs = [ target ],
            appendTask = True
        )

    def connectModules( self, world ):
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
