from entities.parts.part import Part
from entities.modules.module import Module
from entities.parts.hull import Hull, BasicHull
from entities.parts.mobility import Mobility, BasicTracks, BasicWheels


class MobileChassis( Module ) :
	def __init__( self, hull: Hull, mobility: Mobility ):
		self._hull = hull
		self._mobility = mobility
		super().__init__( [ self._hull, self._mobility ] )

	def mobility( self ) -> Part:
		return self._mobility

	def hull( self ) -> Part:
		return self._hull

	@property
	def axisPart( self ) -> Part:
		return self.hull()


class BasicTracksChassis( MobileChassis ):
	def __init__( self ):
		super().__init__( BasicHull(), BasicTracks() )


class BasicWheelsChassis( MobileChassis ):
	def __init__( self ) :
		super().__init__( BasicHull(), BasicWheels() )
