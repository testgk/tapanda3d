from moverdetectors import Detectors
from entities.entity import Entity, entitypart
from entities.modules.turret import CannonTurret
from entities.full.entitywithturret import EntityWithTurret
from entities.parts.part import Part


class Tower( EntityWithTurret, Entity ):
    def __init__( self, turret, towerBase ) -> None:
        super().__init__( turret = turret, axis = towerBase )
        Entity.__init__( self )
        self.__render = None
        self.__detectors = None

    @entitypart
    def towerBase( self ) -> Part:
        return self._axis

    def _setCoreBodyPath( self ):
        self._corePart = self._axis

    def _connectModules( self, world, axis ):
        return super()._connectModules( world, axis = axis )

    def completeLoading( self, physicsWorld, render, terrainSize ) -> None:
        self._setCoreBodyPath()
        self._createModelBounds()
        self.__render = render
        self._initMovementManager( physicsWorld )
        self._createStateMachine()
        self._connectModules( physicsWorld, axis = self._axis )
        self.__detectors = Detectors( self.coreBodyPath, self._length, self._width, self.__render )

    def _initStatesPool( self ):
        self._statesPool = {
        }

    def _createStateMachine( self ):
        pass


class TowerSmall( Tower ):
    def __init__( self ):
        Tower.__init__( self, turret = CannonTurret( scale = 2, mass = 10000), towerBase = TowerBase() )

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
