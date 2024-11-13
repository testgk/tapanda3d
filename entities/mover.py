from entities.parts.engine import Engine
from entities.entity import Entity, entitypart
from entities.parts.part import Part
from movement.movementmgr import MovementManager


class Mover( Entity ):
    def __init__( self, engine, mobility, hull ):
        super().__init__()
        self._currentPosition = None
        self._engine = engine
        self._mobility = mobility
        self._hull = hull
        self._movementManager = MovementManager( self )
        self._corePart = self.mobility()
        self._isMover = True

    def move( self, destination ):
        pass

    def stop( self ):
        pass

    def rotate( self, degrees = 0 ):
        self._movementManager.rotate( degrees )

    def track_target_angle( self, degrees, task ):
        if self._movementManager.track_target_angle( degrees ):
            return task.done
        return task.cont

    def maintain_velocity( self, velocity, angle, task ):
        self._movementManager.velocity( velocity, angle = angle  )
        return task.cont

    @entitypart
    def hull( self ) -> Part:
        return self._hull

    @entitypart
    def mobility( self ) -> Part:
        return self._mobility

 #   @entitypart
    def engine( self ) -> Engine:
        return self._engine
