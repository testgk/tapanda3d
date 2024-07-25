from entities.entity import Entity


class Mover( Entity ):
    def __init__( self, engine, chassis ):
        super().__init__()
        self._currentPosition = None
        self._engine = engine
        self._chassis = chassis

    def move(self, destination ):
        pass

    def stop(self):
        pass

    def turn( self, degrees ):
        pass
