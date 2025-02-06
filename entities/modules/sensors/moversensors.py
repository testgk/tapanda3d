from entities.entity import Entity


class Sensors:
	def __init__( self, entity: Entity ):
		self._entity = entity
		self._edge = None
		self._targetSensor = None
		self._dynamicDetector = None
		self._generateSensors()

	def _generateSensors( self ):
		pass