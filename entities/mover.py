from entities.parts.engine import Engine
from entities.entity import Entity, entitypart
from movement.movementmgr import MovementManager


class Mover( Entity ):
    def __init__( self, engine, mobility, hull ):
        super().__init__()
        self._currentPosition = None
        self._engine = engine
        self._mobility = mobility
        self._hull = hull
        self._movementManager = MovementManager()

    def move( self, destination ):
        pass

    def stop( self ):
        pass

    def turn( self, degrees ):
        pass

    @entitypart
    def hull( self ):
        return self._hull

    @entitypart
    def mobility( self ):
        return self._mobility

 #   @entitypart
    def engine( self ) -> Engine:
        return self._engine
