from panda3d.core import Vec3

from selectionitem import SelectionItem


class Target( SelectionItem ):
	def __init__( self ):
		super().__init__()

	@property
	def position( self ):
		return NotImplemented


class CustomTarget( Target ):
	def __init__( self, position: Vec3 ):
		super().__init__()
		self.__position = position

	@property
	def position( self ) -> Vec3:
		return self.__position
