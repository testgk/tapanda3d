from entities.entity import Entity, entitypart
from entities.modules.chassis import Chassis
from entities.modules.turret import CannonTurret
from entities.full.entitywithturret import EntityWithTurret
from entities.parts.part import Part



class Tower( EntityWithTurret, Entity ):
    def __init__( self, turret, towerBase ) -> None:
        super().__init__(  turret = turret, chassis = towerBase )
        Entity.__init__( self )
        self._corePart = self._chassis

    @entitypart
    def towerBase( self ) -> Part:
        return self._chassis


class TowerSmall( Tower ):
    def __init__( self ):
        Tower.__init__( self, turret = CannonTurret(), towerBase = TowerBase() )


class TowerBase( Part ):
    def __init__( self ):
        super().__init__( partId = "tower_small_base" )

    @property
    def objectPath( self ) -> str:
        return "towerbase"

