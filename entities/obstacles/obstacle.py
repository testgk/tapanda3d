from entities.locatorMode import Locators


class Obstacle:

	def __init__( self ):
		pass

	@property
	def detection( self ) -> Locators:
		return self.__detection

	@detection.setter
	def detection( self, detection: Locators ):
		self.__detection = detection
