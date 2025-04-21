import random
import time
from abc import abstractmethod
from collections import deque
from typing import NoReturn

from panda3d.bullet import BulletRigidBodyNode
from panda3d.core import NodePath, TransparencyAttrib

from entities.partfactory import PartFactory
from entities.parts.part import Part
from enums.colors import Color
from scheduletask import scheduleTask
from selection.selectionitem import SelectionItem
from selection.selectionmodes import SelectionModes
from statemachine.state import State
from statemachine.statemachine import StateMachine
from states.mover.idlestate import IdleState


def entitypart( func ):
	func._is_entitypart = True
	return func




class Entity( SelectionItem ):
	def __init__( self ):
		super().__init__()
		self.__visible = True
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
		self._visibilityTime = time.time()

	@abstractmethod
	def _setCorePart( self ):
		pass

	@property
	def width( self ):
		return self._width

	@property
	def height( self ):
		return self._length

	@property
	def rigidBodyNodes( self ) -> dict[ str: { BulletRigidBodyNode, list[ 'Part' ] } ]:
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
		scheduleTask( self, self._stateMachine.startMachine, appendTask = True )

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

	def _setDamping( self ):
		self.coreRigidBody.set_linear_damping( 0 )
		self.coreRigidBody.set_angular_damping( 0 )

	def isSelected( self, mode: SelectionModes = None ) -> bool:
		return self._selectionMode != SelectionModes.NONE

	def handleSelection( self, mode: SelectionModes = SelectionModes.ANY ):
		self.handleDetection()
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

	def _initStatesPool( self ):
		self._statesPool = {
			"idle" : IdleState,
		}

	def completeLoading( self, physicsWorld, render, terrainSize ) -> None:
		pass

	def selectItem( self, item: 'SelectionItem' ) -> SelectionItem | None:
		raise NotImplementedError

	def _createModelBounds( self ):
		self.__modelBounds = self.coreBodyPath.getTightBounds()
		self._width = ( self.__modelBounds[ 1 ].y - self.__modelBounds[ 0 ].y )
		self._length = ( self.__modelBounds[ 1 ].x - self.__modelBounds[ 0 ].x )
		self._height = ( self.__modelBounds[ 1 ].z - self.__modelBounds[ 0 ].z )

	def _initMovementManager( self, physicsWorld ):
		pass

	def _connectModules( self, physicsWorld ):
		pass

	def detectorColor( self ):
		return None

	def handleDetection( self ):
		self._visibilityTime = time.time()
		self.show()

	def scheduleVisibility( self ):
		scheduleTask( self, self.visibilityTask )

	def visibilityTask( self, task ):
		task.delayTime = 1
		if time.time() - self._visibilityTime > 5:
			self.hide()
		return task.again

	def hide( self ):
		if not self.__visible:
			return
		self.__visible = False
		for model in self.__models:
			r, g, b, a = model.getColor()
			if a != 0.5:
				model.setColor( r, g, b, 0.5 )

	def show( self ):
		if self.__visible:
			return
		self.__visible = True
		for model in self.__models:
			r, g, b, a = model.getColor()
			if a != 1:
				model.setColor( r, g, b, 1 )