from enums.colors import Color
from entities.parts.part import Part
from entities.entity import Entity, entitypart
from selection.selectionitem import SelectionItem
from selection.selectionmodes import SelectionModes


class CubePart( Part ):
	def __init__( self, scale ):
		super( CubePart, self ).__init__( partId = "cube", scale = scale )
		self._objectPath = "obstacles"
		self._color = Color.GREEN
		self._mass = 20000


class Cube( Entity, SelectionItem ):
	def __init__( self, scale = 1 ):
		super().__init__()
		self._cube = CubePart( scale = scale )
		self._corePart = self._cube

	@entitypart
	def cubePart( self ):
		return self._cube

	@property
	def model( self ):
		return self._cube.model

	def show( self ):
		print( f'{ self.name } hit')

	def handleSelection( self, mode: SelectionModes = SelectionModes.ANY ):
		self.model.setColor( Color.MAGENTA )

	def clearSelection( self ):
		self.model.setColor( self.cubePart().color )

	def _createStateMachine( self ):
		pass

class BigCube( Cube ):
	def __init__( self ):
		super().__init__( scale = 2 )

