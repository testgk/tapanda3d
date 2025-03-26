from math import cos, radians, sin

from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import Vec3

from entities.full.movers.mover import DetectorLimits, create_and_setup_sphere
from entities.locatorMode import Locators
from enums.colors import Color


class Detectors:
	def __init__( self ):
		self.__angle_increment = None
		self.__horizontalAngle = None
		self._width = None
		self._length = None
		self.__rightEdge = None
		self.__rightDetector = None
		self.__leftEdge = None
		self.__leftDetector = None
		self.__render = None
		self.__edge = None
		self.__dynamicDetector = None

	@property
	def dynamicDetector( self ):
		return self.__dynamicDetector

	def edgePos( self ):
		return self.__edge.get_pos( self.__render )

	def __getLeftDetectorDirection( self ):
		leftPos = self.__leftDetector.get_pos( self.__render )
		edgePos = self.__leftEdge.get_pos( self.__render )
		return edgePos, leftPos

	def __getRightDetectorDirection( self ):
		rightPos = self.__rightDetector.get_pos( self.__render )
		edgePos = self.__rightEdge.get_pos( self.__render )
		return edgePos, rightPos

	def __getDynamicDetectorDirection( self ):
		dynamicPos = self.__dynamicDetector.get_pos( self.__render )
		edgePos = self.edgePos()
		return edgePos, dynamicPos

	@property
	def rightDetector( self ):
		return self.__rightDetector


	def __createEdges( self ):
		self.__edge = create_and_setup_sphere( self.coreBodyPath, Color.RED, Vec3( self._length / 2, 0, 0 ) )
		self.__targetDetector = create_and_setup_sphere( self.coreBodyPath, Color.ORANGE, Vec3( self._length, 0, 0 ) )
		self.__leftEdge = create_and_setup_sphere( self.coreBodyPath, Color.CYAN,
		                                           Vec3( self._length / 2, self._width / 2, 0 ) )
		self.__rightEdge = create_and_setup_sphere( self.coreBodyPath, Color.CYAN,
		                                            Vec3( self._length / 2, - self._width / 2, 0 ) )
		self.__leftDetector = create_and_setup_sphere( self.coreBodyPath, Color.RED,
		                                               Vec3( self._length, self._width / 2, 0 ) )
		self.__rightDetector = create_and_setup_sphere( self.coreBodyPath, Color.BLUE,
		                                                Vec3( self._length, - self._width / 2, 0 ) )
		self.__dynamicDetector = create_and_setup_sphere( self.coreBodyPath, Color.YELLOW, Vec3( 0, 0, 0 ) )
		taskMgr.add( self.moveDynamicDetector, "CircularMotionTask" )

	def moveDynamicDetector( self, task ):
		if self.freezeDetector:
			return task.cont
		task.delayTime = 0.01
		self.__verticalAngle += self.__angle_increment
		if self.__verticalAngle >= self.__rightLimit or self.__verticalAngle <= self.__leftLimit:
			self.__angle_increment *= -1
		self.__setDynamicDetectorPosition( self.__verticalAngle )
		return task.again

	def __setDynamicDetectorPosition( self, verticalAngle ):
		radians_angle = radians( verticalAngle )
		self.__dynamicDetector.setPos( self._length / 2 + self._width * cos( radians_angle ),
		                               self._width * sin( radians_angle ),
		                               self.__horizontalAngle )

	def setDynamicDetector( self, mode: Locators, freeze = False ):
		self.freezeDetector = freeze
		if mode == Locators.Left:
			self.__leftLimit = 0
			self.__rightLimit = DetectorLimits.Wide
			self.__verticalAngle = 80
			self.__setDynamicDetectorPosition( self.__verticalAngle )
		elif mode == Locators.Right:
			self.__leftLimit = -DetectorLimits.Wide
			self.__rightLimit = 0
			self.__verticalAngle = -80
			self.__setDynamicDetectorPosition( self.__verticalAngle )
		elif mode == Locators.Full:
			self.__verticalAngle = 0
			self.__rightLimit = DetectorLimits.Normal
			self.__leftLimit = -DetectorLimits.Normal
