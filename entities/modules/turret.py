from entities.modules.module import Module
from entities.parts.cannon import ShellCannon
from entities.parts.part import Part
from enums.colors import Color


class Turret( Module ):
    def __init__( self, device: Part ):
        self.__turretBase = TurretBase()
        self.__cannon = device
        super().__init__( [ self.__turretBase , device ])


    @property
    def turretBase( self ):
        return self.__turretBase

    @property
    def turretCannon( self ):
        return self.__cannon


class CannonTurret( Turret ):
    def __init__( self ):
        super().__init__( ShellCannon() )


class TurretBase( Part ):
    def __init__( self ):
        super().__init__( partId = "turret_base" )
        self._color = Color.RED.value

    @property
    def objectPath( self ) -> str:
        return "turret"
