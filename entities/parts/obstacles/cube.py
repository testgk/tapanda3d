from entities.parts.abstract.cubepart import CubePart
from enums.colors import Color
from entities.entity import entitypart, Entity
from selection.selectionitem import SelectionItem
from selection.selectionmodes import SelectionModes


class Cube( Entity, SelectionItem ):
	def __init__( self, scale = 1 ):
		super().__init__()
		self._cube = CubePart( scale = scale )
		self._corePart = self._cube

	@entitypart
	def selectionPart( self ):
		return self._cube

	@property
	def model( self ):
		return self._cube.model

	def show( self ):
		print( f'{ self.name } hit')

	def handleSelection( self, mode: SelectionModes = SelectionModes.ANY ):
		self._selectionMode = mode
		self.model.setColor( Color.MAGENTA )

	def handleDetection( self ):
		self.model.setColor( Color.ORANGE )

	def clearSelection( self ):
		self.model.setColor( self.selectionPart().color )

	def _createStateMachine( self ):
		pass

class BigCube( Cube ):
	def __init__( self ):
		super().__init__( scale = 2 )

