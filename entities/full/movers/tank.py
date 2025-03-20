from entities.entity import entitypart
from entities.modules.turret import Turret
from entities.full.attacker import Attacker
from entities.full.movers.mover import Mover
from entities.modules.chassis import Chassis
from entities.full.entitywithturret import EntityWithTurret


class Tank( Mover, Attacker, EntityWithTurret ):
    def __init__( self, engine, chassis: Chassis, turret: Turret ):
        super().__init__( chassis = chassis, engine = engine )
        EntityWithTurret.__init__( self, chassis, turret )


    @entitypart
    def cannon( self ):
        return self._turret.turretCannon