from entities.mover import Mover, entitypart
from entities.parts.turret import Turret


class Tank( Mover ):
    def __init__( self, engine, chassis, turret ):
        super().__init__( chassis = chassis, engine = engine  )
        self.__turret = turret
        self.parts = [ 'body', 'turret' ]

    @property
    @entitypart
    def turret( self ) -> Turret:
        return self.__turret
