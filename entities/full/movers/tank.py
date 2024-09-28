from entities.entity import entitymodule
from entities.mover import Mover
from entities.modules.turret import Turret
from entities.parts.hull import BasicHull


class Tank( Mover ):
    def __init__( self, engine, mobility, turret ):
        super().__init__( mobility = mobility, engine = engine, hull = BasicHull() )
        self.__turret = turret

    @entitymodule
    def turret( self ) -> Turret:
        return self.__turret

