from entities.modules.chassis import Chassis
from entities.parts.engine import Engine
from entities.entity import Entity, entitypart, entitymodule
from entities.parts.part import Part
from movement.movementmgr import MovementManager
from selectionmodes import SelectionModes
from statemachine.state import State
from states.idlestate import IdleState
from states.movementstate import MovementState


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

    def rotate( self, degrees = 0 ):
        self._movementManager.rotate( degrees )

    def monitorIdleState( self, task ):
        if not self.isSelected( mode = SelectionModes.P2P ):
            return task.cont
        if self.selectTargets.empty():
            return task.cont
        print( f'{ self.name } moving p2p to { self.selectTargets }' )
        self.readyToMove = True
        return task.done

    def decide( self, currentState: 'State' ) -> str:
        if currentState == "MovementState":
            return "idle"

    def initStatesPool( self ):
        self._statesPool = {
            "idle": IdleState( self ),
            "movement": MovementState( self ),
        }

    def scheduleIdleMonitoringTask( self ):
        self.scheduleTask( self.monitorIdleState, "monitoring command" )

    def schedulePointToPointTask( self ):
        position = self.selectTargets.get().position
        self.scheduleTask(
            self._movementManager.set_velocity_toward_point_with_stop,
            f"{ self.name }_move_p2p",
            extraArgs = [ position ],
            appendTask = True
        )
        self.scheduleTask(
            self._movementManager.track_target_angle,
            f"{ self.name }_monitor_angle",
            extraArgs = [ position ],
            appendTask = True
        )

    def finishedMovement( self ):
        if self._taskMgr.hasTaskNamed( f"{ self.name }_move_p2p" ):
            return False
        self.readyToMove = False
        return True

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
