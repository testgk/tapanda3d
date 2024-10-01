from entities.parts.engine import Engine
from entities.entity import Entity, entitypart


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

    @property
    @entitypart
    def chassis( self ):
        return self._chassis

    @property
    @entitypart
    def engine( self ) -> Engine:
        return self._engine
