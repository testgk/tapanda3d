from entities.parts.module import Module
from entities.parts.cannon import ShellCannon


class Turret( Module ):
	def __init__( self, device ):
		super().__init__( device )
		self.__device = device

	def device( self ):
		return self.__device


class CannonTurret( Turret ) :
	def __init__( self ) :
		super().__init__( ShellCannon() )
