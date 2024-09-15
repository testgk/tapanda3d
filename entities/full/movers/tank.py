from entities.entity import entitymodule
from entities.mover import Mover
from entities.modules.turret import Turret


class Tank( Mover ):
    def __init__( self, engine, mobility, turret ):
        super().__init__( mobility = mobility, engine = engine )
        self.__turret = turret

    @entitymodule
    def turret( self ) -> Turret:
        return self.__turret
