from abc import ABC

from movement.towermovementmanager import TowerMovementManager
from moverdetectors import Detectors
from entities.entity import Entity, entitypart
from entities.modules.turret import CannonTurret
from entities.entitywithturret import EntityWithTurret
from entities.parts.part import Part
from scheduletask import scheduleTask
from selection.selectionitem import SelectionItem
from selection.selectionmodes import SelectionModes
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
        self.__detectors = None
        turret.name = f"{ self.name }_turret"
        towerBase.name = f"{ self.name }_tower"

    @entitypart
    def towerBase( self ) -> Part:
        return self._axis

    @property
    def currentTarget( self ) -> Target:
        return self.__currentTarget

    def _setCorePart( self ):
        self._corePart =  self.turretBase()

    def _connectModules( self, world, axis ):
        return super()._connectModules( world, axis = axis )

    def completeLoading( self, physicsWorld, render, terrainSize ) -> None:
        self.__render = render
        self._setCorePart()
        self._createModelBounds()
        self._initMovementManager( physicsWorld )
        self._createStateMachine()
        self._connectModules( physicsWorld, axis = self._axis )
        self.__detectors = Detectors( self.coreBodyPath, self._length, self._width, self.__render )

    def _initMovementManager( self, physicsWorld ):
        self._movementManager = TowerMovementManager( self )

    def _createStateMachine( self ):
        self._stateMachine = StateMachine( self, initState = TowerIdleState( entity = self ) )
        scheduleTask( self, self._stateMachine.startMachine, appendTask = True )

    def selectItem( self, item: 'SelectionItem' ) -> SelectionItem | None:
        if item == self:
            self.clearSelection()
            return None

        if not item.isTerrain:
            self._selectedTargets.appendleft( item )
            item.handleSelection( SelectionModes.ATTACK )
            return self

    def scheduleTargetMonitoringTask( self ):
        scheduleTask( self, self.targetMonitoringTask, checkExisting = True )

    def targetMonitoringTask( self, task ):
        if self.__nextTarget is None and any( self._selectedTargets ):
            self.__nextTarget = self._selectedTargets.pop()
            return task.cont

        if self.__currentTarget is None:
            self.__currentTarget = self.__nextTarget
            self.__nextTarget = None
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
        self._scale = 5
        self._mass = 20000

    @property
    def objectPath( self ) -> str:
        return "towerbase"
