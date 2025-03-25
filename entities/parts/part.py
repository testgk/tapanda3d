from enums.colors import Color
from panda3d.core import BitMask32, LVector3, NodePath

from collsiongroups import CollisionGroup


class Part:

	def __init__( self, partData = None,
	              partId: str = None,
	              **kwargs ):
		self.__rigidGroup = self.__class__.__name__
		self.__collideGroup = CollisionGroup.MODEL
		self.__partId = partId
		self.__model = None
		self.__rigidBody = None
		self.__rigidBodyPath = None
		self._objectPath = kwargs.get( 'path', None ) or self.__class__.__name__.lower()
		self._color = kwargs.get( 'color', None ) or Color.RED
		self.__mass = kwargs.get( 'mass', None ) or 50
		if partId and partData:
			part_data = partData.get( partId )
			self._readPartData( part_data )
		self.__friction = 0
		self._scale = 1

	@property
	def objectPath( self ) -> str:
		return self._objectPath

	@property
	def rigidBodyPath( self ):
		return self.__rigidBodyPath

	@rigidBodyPath.setter
	def rigidBodyPath( self, path ) -> None:
		self.__rigidBodyPath = path

	@property
	def rigidBody( self ):
		return self.__rigidBody

	@rigidBody.setter
	def rigidBody( self, path ) -> None:
		self.__rigidBody = path

	@property
	def rigidGroup( self ) -> str:
		return self.__rigidGroup

	@property
	def partId( self ) -> str:
		return self.__partId

	@property
	def color( self ):
		return self._color

	@property
	def mass( self ):
		return self.__mass

	@property
	def model( self ) -> NodePath:
		return self.__model

	@property
	def collideGroup( self ):
		return self.__collideGroup

	@model.setter
	def model( self, value ):
		self.__model = value

	@property
	def scale( self ):
		return self._scale

	def setRigidBodyProperties( self, rigidBody ):
		self.__rigidBody = rigidBody
		self.__rigidBody.setIntoCollideMask( BitMask32.allOff() )
		self.__rigidBody.setIntoCollideMask( self.collideGroup )
		self.__rigidBody.setMass( self.__rigidBody.mass + self.mass )

	def _readPartData( self, part_data ):
		self.__metal = part_data[ "metal" ]
		self.__energy = part_data[ "energy" ]
		self.__mass = part_data.get( "mass", self.__mass )
		self.__protection = part_data.get( "protection", 0 )
		self.__damage = part_data.get( "damage", 0 )
		self.__friction = part_data.get( "friction", LVector3( 0.01, 10, 0.0 ) )

	@rigidGroup.setter
	def rigidGroup( self, value ):
		self.__rigidGroup = value

	@collideGroup.setter
	def collideGroup( self, value ):
		self.__collideGroup = value

	@scale.setter
	def scale( self, value ):
		self._scale = value

	@mass.setter
	def mass( self, value ):
		self._mass = value
