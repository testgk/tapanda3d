from entities.parts.engine import Engine
from entities.entity import Entity, entitypart


class Mover( Entity ):
    def __init__( self, engine, mobility ):
        super().__init__()
        self._currentPosition = None
        self._engine = engine
        self._mobility = mobility

    def move(self, destination ):
        pass

    def stop(self):
        pass

    def turn( self, degrees ):
        pass

    @entitypart
    def mobility( self ):
        return self._mobility

    @entitypart
    def engine( self ) -> Engine:
        return self._engine
