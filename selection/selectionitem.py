import queue
from collections import deque
from selectionmodes import SelectionModes


class SelectionItem:
	def __init__( self ):
		self._isMover = False
		self._isTerrain = False
		self._selectionMode = SelectionModes.NONE
		self._moveTargets: deque = deque()
		self._selectTargetPositions: queue.Queue = queue.Queue()

	@property
	def isMover( self ) -> bool:
		return self._isMover

	@property
	def isTerrain( self ) -> bool:
		return self._isTerrain

	def isSelected( self, mode: SelectionModes = SelectionModes.ANY ) -> bool:
		if mode == SelectionModes.ANY:
			return self._selectionMode != SelectionModes.NONE
		return self._selectionMode == mode

	def selectItem( self, item: 'SelectionItem' ) -> None:
		raise NotImplementedError

	def handleSelection( self, mode: SelectionModes = SelectionModes.ANY ):
		raise NotImplementedError

	def clearSelection( self ):
		raise NotImplementedError


