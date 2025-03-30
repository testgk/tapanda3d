import random
from abc import abstractmethod
from collections import deque
from typing import NoReturn

from direct.task.TaskManagerGlobal import taskMgr
from panda3d.bullet import BulletRigidBodyNode
from panda3d.core import NodePath

from entities.partfactory import PartFactory
from entities.commandmanager import CommandManager
from entities.parts.part import Part
from movement.towermovementmanager import TowerMovementManager
from selectionitem import SelectionItem
from selectionmodes import SelectionModes
from statemachine.state import State
from statemachine.statemachine import StateMachine
from states.mover.idlestate import IdleState


def entitypart( func ):
	func._is_entitypart = True
	return func




class Entity( SelectionItem ):
	def __init__( self ):
		super().__init__()
		self._selectedTargets: deque = deque()
		self._scale = 1
		self._statesPool: dict = {}
		self._stateMachine = None
		self.name = f'{ self.__class__.__name__}_{ random.randint(1, 1000 ) }'
		self._id = None
		self.__models = [ ]
		self._partBuilder = PartFactory( self )
		self.__collisionBox = None
		self.__rigidBodies : dict[ str: { BulletRigidBodyNode, list[ 'Part' ] } ] = None
		self._corePart = None
		self._coreBodyPath = None
		self._isMover = False
		self._initStatesPool()
		self._length = None
		self._width = None
		self._height = None

	@abstractmethod
	def _setCoreBodyPath( self ):
		pass

	@property
	def width( self ):
		return self._width

	@property
	def height( self ):
		return self._length

	@property
	def rigidBodyNodes( self )  -> dict[ str: { BulletRigidBodyNode, list[ 'Part' ] } ]:
		return self.__rigidBodies

	@property
	def isObstacle( self ):
		return True

	@property
	def coreBodyPath( self ) -> NodePath | NoReturn:
		if self._corePart:
			return self._corePart.rigidBodyPath

	@property
	def coreRigidBody( self ) -> BulletRigidBodyNode | NoReturn:
		if self._corePart:
			return self._corePart.rigidBody

	@property
	def selectBox( self ):
		try:
			return self.__collisionBox
		except IndexError:
			return None

	@abstractmethod
	def getFamilyType( self ):
		raise NotImplementedError()

	def _createStateMachine( self ):
		self._stateMachine = StateMachine( self, initState = IdleState( entity = self ) )
		self.scheduleTask( self._stateMachine.startMachine, appendTask = True )

	@property
	def position( self ):
		if self.coreBodyPath:
			return self.coreBodyPath.get_pos()

	@property
	def models( self ):
		return self._partBuilder.models

	def buildModels( self, loader ):
		self._partBuilder.build( loader )
		self.__models = self._partBuilder.models
		self.__collisionBox = self._partBuilder.collisionBox()
		self.__collisionBox.setPythonTag( 'collision_target', self )
		self.__rigidBodies = self._partBuilder.rigidBodies()

	def decide( self, currentState: State ) -> str:
		raise NotImplementedError

	def getStateFromEntityPool( self, stateName: str ):
		return self._statesPool[ stateName ]

	def scheduleTask( self, method, extraArgs: list = None, appendTask = True, checkExisting = False ):
		name = f'{ self.name }_{ method.__name__ }'
		if checkExisting:
			if taskMgr.hasTaskNamed( name ):
				return
		taskMgr.add( method, name = f'{ self.name }_{ method.__name__ }', extraArgs = extraArgs, appendTask = appendTask )

	def _setDamping( self ):
		self.coreRigidBody.set_linear_damping( 0 )
		self.coreRigidBody.set_angular_damping( 0 )

	def isSelected( self, mode: SelectionModes = None ) -> bool:
		return self._selectionMode != SelectionModes.NONE

	def handleSelection( self, mode: SelectionModes = SelectionModes.ANY ):
		if self.isSelected( mode ):
			self.clearSelection()
		print( f'{ self.name } is selected' )
		self._selectionMode = SelectionModes.P2P
		self.selectBox.show()

	def clearSelection( self ):
		self._selectionMode = SelectionModes.NONE
		for model in self.__models:
			part = model.node().getPythonTag( 'model_part' )
			model.setColor( part.color )
		if self.__collisionBox:
			self.__collisionBox.hide()

	def selectItem( self, item: 'SelectionItem' ) -> SelectionItem | None:
		if item == self:
			self.clearSelection()
		if item != self and item.isMover:
			item.handleSelection( SelectionModes.ANY )
			self.clearSelection()
			return item
		if item.isTerrain:
			if self.isMover:
				self._selectedTargets.appendleft( item )
				item.handleSelection( SelectionModes.P2P )
				return self
			else:
				self.clearSelection()
				item.handleSelection( SelectionModes.CREATE )
				return item
		return None

	def _initStatesPool( self ):
		self._statesPool = {
			"idle" : IdleState,
		}

	def isValidState( self, stateName ) -> bool:
		return stateName in self._statesPool

	def completeLoading( self, physicsWorld, render, terrainSize ) -> None:
		pass

	def _createModelBounds( self ):
		self.__modelBounds = self.coreBodyPath.getTightBounds()
		self._width = ( self.__modelBounds[ 1 ].y - self.__modelBounds[ 0 ].y )
		self._length = ( self.__modelBounds[ 1 ].x - self.__modelBounds[ 0 ].x )
		self._height = ( self.__modelBounds[ 1 ].z - self.__modelBounds[ 0 ].z )

	def _initMovementManager( self, physicsWorld ):
		pass

	def _connectModules( self, physicsWorld ):
		pass
