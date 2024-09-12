from entities.parts.part import Part
#from entities.partfactory import PartFactory


class Module:
	def __init__( self, device: Part ):
		self.__device = device
		#self.__partFactory = PartFactory( self )