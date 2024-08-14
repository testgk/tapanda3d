from entities.mover import Mover


class Tank( Mover ):
    def __init__( self, engine, chassis, turret ):
        super().__init__( chassis = chassis, engine = engine  )
        self.__turret = turret
        self.parts = [ 'body', 'turret' ]

    @property
    def chassis( self ):
        return self._chassis

    @property
    def turret( self ) -> Turret:
        return self.__turret
