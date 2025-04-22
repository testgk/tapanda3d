from entities.parts.part import Part
from entities.parts.database import parts


class Ammunition:
	pass


class Cannon( Part ) :
	def __init__( self, barrelId: str, ammunition: Ammunition ) :
		self._objectPath = "barrels"
		self._ammunition = ammunition
		super().__init__( parts.CANNONS, partId = barrelId )

	@property
	def objectPath( self ) -> str:
		return "barrels"

	def _readPartData( self, part_data ):
		super()._readPartData( part_data )

	def shoot( self ):
		raise NotImplementedError


class LaserCannon( Cannon ):
	def __init__( self ) :
		super().__init__( "laser_cannon", None )

class ShellCannon( Cannon ):
	def __init__( self ):
		super().__init__( "shell_cannon", None )
