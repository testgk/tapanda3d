from collsiongroups import CollisionGroup
from entities.parts.part import Part


class Module:
	def __init__( self, devices: Part | list[ Part ], collideGroup: CollisionGroup = CollisionGroup.MODEL ):
		self._collideGroup = collideGroup
		self.__devices: list[ Part ] = []
		self.__devices.extend( devices if isinstance( devices, list ) else [ devices ] )
		for device in self.__devices:
			device.rigidGroup = self.__class__.__name__
			device.collideGroup = self._collideGroup

	@property
	def devices( self ) -> list[ Part ]:
		return self.__devices