from entities.parts.part import Part


class Module:
	def __init__( self, device: Part ):
		self.__device = device

	@property
	def device( self ) -> Part:
		return self.__device