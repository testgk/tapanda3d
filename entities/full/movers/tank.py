from entities.entity import entitymodule, entitypart
from entities.full.movers.mover import Mover
from entities.modules.chassis import Chassis
from entities.modules.turret import Turret, TurretBase
from entities.parts.rolls import Rolls


class Tank( Mover ):
    def __init__( self, engine, chassis: Chassis, turret: Turret ):
        super().__init__( chassis = chassis, engine = engine )
        self.__turret = turret

    @entitymodule
    def turret( self ) -> Turret:
        return self.__turret

    @entitypart
    def turretBase( self ):
        return self.__turret.turretBase

    def reparentModels( self ):
        pass

