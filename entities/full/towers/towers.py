from abc import ABC

from detection.detector import Detector
from detection.sensors import Senesors
from detection.towersensors import TowerSensors
from movement.towermovementmanager import TowerMovementManager
from entities.entity import Entity, entitypart
from entities.modules.turret import CannonTurret
from entities.entitywithturret import EntityWithTurret
from entities.parts.part import Part
from scheduletask import scheduleTask
from selection.selectionitem import SelectionItem
from statemachine.statemachine import StateMachine
from states import States
from states.tower.toweridlestate import TowerIdleState
from target import Target


class Tower( EntityWithTurret, Entity, ABC ):
    def __init__( self, turret, towerBase ) -> None:
        super().__init__( turret = turret, axis = towerBase )
        Entity.__init__( self )
        self.__nextTarget = None
        self.__currentTarget = None
        self.__render = None
        self.__sensors = None
        turret.name = f"{ self.name }_turret"
        towerBase.name = f"{ self.name }_tower"


    @entitypart
    def towerBase( self ) -> Part:
        return self._axis

    @property
    def sensors( self ) -> Senesors:
        return self.__sensors

    @property
    def currentTarget( self ) -> Target:
        return self.__currentTarget

    def _setCorePart( self ):
        self._corePart = self.turretBase()

    def _connectModules( self, world ):
        return super()._connectTurret( world, axis = self._axis )

    def completeLoading( self, physicsWorld, render, terrainSize ) -> None:
        self.__render = render
        self._setCorePart()
        self._createModelBounds()
        self._initMovementManager( physicsWorld )
        self.__sensors = TowerSensors( self.coreBodyPath, self._length, self._width, self._height, self.__render )
        self._createStateMachine()
        self._connectModules( physicsWorld )
        #self.scheduleVisibility()

    def _initMovementManager( self, world ):
        self._movementManager = TowerMovementManager( self, world, self.__render )

    def _createStateMachine( self ):
        self._stateMachine = StateMachine( self, initState = TowerIdleState( entity = self ) )
        scheduleTask( self, self._stateMachine.startMachine, appendTask = True )

    def selectItem( self, item: 'SelectionItem' ) -> SelectionItem | None:
        if item == self:
            self.clearSelection()
            return None

        self._selectedTargets.appendleft( item )
        #item.handleSelection( SelectionModes.ATTACK )
        return self

    def clearCurrentTarget( self ):
        if not self.__currentTarget:
            return
        if self.__currentTarget is self.__nextTarget:
            self.__nextTarget = None
        self.__currentTarget = None

    def scheduleTargetMonitoringTask( self ):
        scheduleTask( entity = self, method = self.targetMonitoringTask, checkExisting = True )
        scheduleTask( entity = self, method = self._movementManager.detectTargets, checkExisting = True )
        scheduleTask( entity = self, method = self._movementManager.isAlignedToTarget, checkExisting = True )

    def targetMonitoringTask( self, task ):
        if self.__nextTarget is None and any( self._selectedTargets ):
            self.__nextTarget = self._selectedTargets.pop()
            return task.cont

        if self.__nextTarget and self.__currentTarget is None:
            self.__currentTarget = self.__nextTarget
            self.__nextTarget = None
            self.aligned = False
        return task.cont

    def _initStatesPool( self ):
        self._statesPool = {
            States.IDLE: TowerIdleState( self )
        }


class TowerSmall( Tower ):
    def __init__( self ):
        Tower.__init__( self, turret = CannonTurret( scale = 2, mass = 10000 ), towerBase = TowerBase() )

    @entitypart
    def cannon( self ):
        return self._turret.turretCannon


class TowerBase( Part ):
    def __init__( self ):
        super().__init__( partId = "tower_small_base" )
        self._scale = 4
        self._mass = 20000

    @property
    def objectPath( self ) -> str:
        return "towerbase"
