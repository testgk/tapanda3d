from entities.locatorMode import Locators
from selection.selectionitem import SelectionItem


class Obstacle( SelectionItem ):

	def __init__( self ):
		super().__init__()
		self.__detection = None

	@property
	def detection( self ) -> Locators:
		return self.__detection

	@detection.setter
	def detection( self, detection: Locators ):
		self.__detection = detection
