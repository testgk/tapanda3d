from entities.modules.chassis import Chassis
from entities.parts.engine import Engine
from entities.entity import Entity, entitypart, entitymodule
from entities.parts.part import Part
from movement.movementmgr import MovementManager


class Mover( Entity ):
    def __init__( self, engine, chassis: Chassis ):
        super().__init__()
        self._chassis = None
        self._currentPosition = None
        self._engine = engine
        self._mobility = chassis.mobility()
        self._hull = chassis.hull()
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

    def maintain_velocity( self, velocity, task ):
        self._movementManager.velocity( velocity  )
        return task.cont

    @entitypart
    def hull( self ) -> Part:
        return self._hull

    @entitypart
    def mobility( self ) -> Part:
        return self._mobility

    @entitymodule
    def chassis( self ) -> Chassis:
        return self._chassis

 #   @entitypart
    def engine( self ) -> Engine:
        return self._engine

    def reparentModels( self ):
        raise NotImplementedError
