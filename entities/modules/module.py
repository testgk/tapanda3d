from collsiongroups import CollisionGroup
from entities.parts.part import Part


class Module:
	def __init__( self, devices: Part | list[ Part ], ** kwargs ):
		self.__name = None
		self._collideGroup = kwargs.get( "collideGroup", CollisionGroup.MODEL )
		self.__devices: list[ Part ] = []
		self.__devices.extend( devices if isinstance( devices, list ) else [ devices ] )
		for device in self.__devices:
			device.rigidGroup = self.__class__.__name__
			device.collideGroup = self._collideGroup
			if device.scale == 1:
				device.scale = kwargs.get( 'scale', 1 )
			device.mass = kwargs.get( 'mass', 0 )

	@property
	def name( self ):
		return self.__name

	@name.setter
	def name( self, name ):
		self.__name = name
