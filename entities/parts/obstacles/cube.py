from enums.colors import Color
from entities.parts.part import Part
from entities.entity import Entity, entitypart


class CubePart( Part ):
	def __init__( self ):
		super( CubePart, self ).__init__( partId = "cube" )
		self._objectPath = "obstacles"
		self._color = Color.GREEN.value
		self._mass = 20000


class Cube( Entity ):
	def __init__( self ):
		super().__init__()
		self._cube = CubePart()
		self._corePart = self._cube
		self._scale = 1

	@entitypart
	def cubePart( self ):
		return self._cube

	def show( self ):
		print( f'{ self.name} hit')
