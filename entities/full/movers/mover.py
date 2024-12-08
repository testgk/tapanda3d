from entities.modules.chassis import Chassis
from entities.parts.engine import Engine
from entities.entity import Entity, entitypart, entitymodule
from entities.parts.part import Part
from movement.movementmgr import MovementManager
from selectionmodes import SelectionModes


class Mover( Entity ):
    def __init__( self, engine, chassis: Chassis ):
        super().__init__()
        self.readyToMove = False
        self._chassis = chassis
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

    def trackPositionCommand( self ):
        return not self.selectTargets.empty()

    def monitorIdleState( self, task ):
        if not self.isSelected( mode = SelectionModes.P2P ):
            return task.cont
        if self.selectTargets.empty():
            return task.cont
        print( f'{ self.name } moving p2p to { self.selectTargets }' )
        self.readyToMove = True
        return task.done

    def schedulePointToPointTask( self ):
        position = self.selectTargets.get().position
        self._taskMgr.add(
            self._movementManager.set_velocity_toward_point_with_stop,
            "move_p2p",
            extraArgs = [ position ],
            appendTask = True
        )

    def finishedMovement( self ):
        return not self._taskMgr.hasTaskNamed( "move p2p" )

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
        print( self.partModels.get( self.chassis ) )

