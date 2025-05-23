from collsiongroups import CollisionGroup
from entities.parts.part import Part
from entities.parts.database import parts
from enums.colors import Color


class Mobility( Part ) :
	def __init__( self, partId ):
		super().__init__( parts.MOBILITY, partId, external = True )
		self._color = Color.YELLOW

	@property
	def objectPath( self ) -> str:
		return "mobility"

	@property
	def friction( self ) -> float:
		return self.__friction

	def _readPartData( self, part_data ):
		self.mobile_ability = part_data[ "mobile_ability" ]
		#self.__friction = part_data[ "friction" ]


class BasicTracks( Mobility ):
	def __init__( self ):
		super().__init__( "basic_tracks" )

	@property
	def objectPath( self ) -> str:
		return "mobility/tracks"


class BasicWheels( Mobility ):
	def __init__( self ) :
		super().__init__( "basic_wheels" )

	@property
	def objectPath( self ) -> str:
		return "mobility/wheels"
