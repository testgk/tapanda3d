from entities.modules.module import Module
from entities.parts.cannon import ShellCannon
from entities.parts.part import Part


class Turret( Module ):
	def __init__( self, devices: Part | list[ Part ] ):
		super().__init__( devices )


class CannonTurret( Turret ) :
	def __init__( self ) :
		super().__init__( ShellCannon() )
