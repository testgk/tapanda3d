from panda3d.core import Vec3

from selection.selectionitem import SelectionItem
from selection.selectionmodes import SelectionModes


class Target:
	def __init__( self, isCustom = False ):
		super().__init__()
		self._isCustom = isCustom

	@property
	def position( self ):
		return NotImplemented

	@property
	def isTerrain( self ):
		return NotImplemented

	def isSelected( self, selectionMode: SelectionModes ):
		raise NotImplementedError()


class CustomTarget( Target, SelectionItem ):
	def __init__( self, position: Vec3 ):
		super().__init__( isCustom = True )
		self.__position = position

	@property
	def position( self ) -> Vec3:
		return self.__position

	def handleSelection( self, mode: SelectionModes = SelectionModes.ANY ):
		pass

