from entities.parts.part import Part
from entities.parts.database import parts


class Cannon( Part ) :
	def __init__( self, barrelId ) :
		super().__init__( parts.CANNONS, partId = barrelId )

	def objectPath( self ) -> str:
		return "cannons"

	def _readPartData( self, part_data ):
		super()._readPartData( part_data )
		self.damagePoints = part_data[ 'damage_points' ]
		self.distance = part_data[ 'distance' ]

	def shoot( self ):
		raise NotImplementedError


class LaserCannon( Cannon ):
	def __init__( self ) :
		super().__init__( "laser_cannon" )

class ShellCannon( Cannon ):
	def __init__( self ):
		super().__init__( "shell_cannon" )


