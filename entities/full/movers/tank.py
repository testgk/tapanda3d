from entities.entity import entitymodule, entitypart
from entities.full.movers.mover import Mover
from entities.modules.chassis import Chassis
from entities.modules.turret import Turret, TurretBase
from entities.parts.rolls import Rolls


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

    def reparentModules( self ):
        hull = self._chassis.hull().model
        turret = self.turretBase().model
        cannon = self.cannon().model
        turret.reparentTo( hull )
        cannon.reparentTo( turret )

