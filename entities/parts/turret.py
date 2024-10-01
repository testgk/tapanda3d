from entities.entity import entitypart
from entities.parts.barrels import ShellCannon
from entities.parts.part import Part
from entities.parts.partsdb import parts


class Turret( Part ):
    def __init__( self, device ):
        super().__init__( partData = parts.TURRETS, device = "turret", external = True )
        self.__device = device

    @property
    @entitypart
    def device( self ):
        return self.__device


class CannonTurret( Turret ):
    def __init__( self ):
        super().__init__( ShellCannon() )