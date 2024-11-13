from selectionmodes import SelectionModes


class SelectionItem:

	def __init__( self ):
		self._isMover = False
		self._isTerrain = False
		self._selectionMode = SelectionModes.NONE

	@property
	def isMover( self ) -> bool:
		return self._isMover

	@property
	def isTerrain( self ) -> bool:
		return self._isTerrain

	def isSelected( self, mode: SelectionModes ) -> bool:
		return self._selectionMode == mode
