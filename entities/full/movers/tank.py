from entities.entity import entitymodule, entitypart
from entities.mover import Mover
from entities.modules.turret import Turret
from entities.parts.hull import BasicHull
from entities.parts.rolls import Rolls


class Tank( Mover ):
    def __init__( self, engine, mobility, turret ):
        super().__init__( mobility = mobility, engine = engine, hull = BasicHull() )
        self.__turret = turret
        self.__frontRolls = Rolls( "front" )
        self.__rearRolls = Rolls( "rear" )

    @entitymodule
    def turret( self ) -> Turret:
        return self.__turret

    @entitypart
    def frontRolls( self ):
        return self.__frontRolls

    @entitypart
    def rearRolls( self ):
        return self.__rearRolls
