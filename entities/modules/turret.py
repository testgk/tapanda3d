from entities.modules.module import Module
from entities.parts.cannon import ShellCannon


class Turret( Module ):
	def __init__( self, device ):
		super().__init__( device )
		self.__device = device


class CannonTurret( Turret ) :
	def __init__( self ) :
		super().__init__( ShellCannon() )
