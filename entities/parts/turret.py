from entities.entity import entitypart
from entities.parts.barrels import ShellCannon
from entities.parts.part import Part


class Turret( Part ):
    def __init__( self, device, ** kwargs ):
        super().__init__( ** kwargs )
        self.__device = device

    @property
    @entitypart
    def device( self ):
        return self.__device


class CannonTurret( Turret ):
    def __init__( self ):
        super().__init__( ShellCannon() )