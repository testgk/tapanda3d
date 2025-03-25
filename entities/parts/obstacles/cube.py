from enums.colors import Color
from entities.parts.part import Part
from entities.entity import Entity, entitypart
from selectionitem import SelectionItem
from selectionmodes import SelectionModes


class CubePart( Part ):
	def __init__( self ):
		super( CubePart, self ).__init__( partId = "cube" )
		self._objectPath = "obstacles"
		self._color = Color.GREEN
		self._mass = 20000


class Cube( Entity, SelectionItem ):
	def __init__( self ):
		super().__init__()
		self._cube = CubePart()
		self._corePart = self._cube
		self._scale = 1

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
