from math import cos, radians, sin

from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import Vec3

from entities.locatorMode import Locators
from enums.colors import Color
from objects.spheres import createAndSetupSphere


class DetectorLimits:
	Wide = 120
	Normal = 45

class TowerSensors:
	def __init__( self, coreBodyPath, length, width, height, render ):
		self.__freezeDetector = None
		self.__leftLimit = None
		self.__rightLimit = None
		self.__horizonAngle = 0
		self.__angle_increment = 2
		self.__verticalAngle = 20
		self._width = width
		self._length = length
		self._height = height
		self.__coreBodyPath = coreBodyPath
		self._detectors = {}
		self._render = render
		self._createDirections()
		self._createDetectors()
		self.setDynamicDetector( Locators.Full )
		taskMgr.add( self.moveDynamicDetector, "CircularMotionTask" )

	@property
	def freezeDetector( self ):
		return self.__freezeDetector

	@freezeDetector.setter
	def freezeDetector( self, freeze: bool ):
		self.__freezeDetector = freeze

	def __edgePos( self ):
		return self._detectors[ "edge" ].get_pos( self._render )

	def _getDynamicDetectorDirection( self ):
		dynamicPos = self._detectors[ "dynamic" ].get_pos( self._render )
		edgePos = self.__edgePos()
		return edgePos, dynamicPos

	def moveDynamicDetector( self, task ):
		if self.__freezeDetector:
			return task.cont
		task.delayTime = 0.01
		self.__horizonAngle += self.__angle_increment
		if self.__horizonAngle >= self.__rightLimit or self.__horizonAngle <= self.__leftLimit:
			self.__angle_increment *= -1
		self.__setDynamicDetectorPosition( self.__horizonAngle )
		return task.again

	def __setDynamicDetectorPosition( self, verticalAngle ):
		radians_angle = radians( verticalAngle )
		self._detectors[ "dynamic" ].setPos( self._length / 2 + self._width * cos( radians_angle ),
		                                     self._width * sin( radians_angle ),
		                                     self._height - self.__verticalAngle )

	def setDynamicDetector( self, mode: Locators, freeze = False ):
		self.__freezeDetector = freeze
		if mode == Locators.Left:
			self.__leftLimit = 0
			self.__rightLimit = DetectorLimits.Wide
			self.__horizonAngle = 80
			self.__setDynamicDetectorPosition( self.__horizonAngle )
		elif mode == Locators.Right:
			self.__leftLimit = -DetectorLimits.Wide
			self.__rightLimit = 0
			self.__horizonAngle = -80
			self.__setDynamicDetectorPosition( self.__horizonAngle )
		elif mode == Locators.Full:
			self.__horizonAngle = 0
			self.__rightLimit = DetectorLimits.Normal
			self.__leftLimit = -DetectorLimits.Normal

	def _createDetector( self, color, position ):
		return createAndSetupSphere( self.__coreBodyPath, color, position )

	def edgePos( self ):
		return self._detectors[ "edge" ].get_pos( self._render )

	def getDirection( self, option ):
		return self._directions[ option ]()

	def _createDetectors( self ):
		self._detectors = {
			"edge": self._createDetector( Color.RED, Vec3( self._length / 2, 0, self._height ) ),
			"target": self._createDetector( Color.ORANGE, Vec3( self._length, 0, self._height ) ),
			"dynamic": self._createDetector( Color.YELLOW, Vec3( 0, 0, self._height ) ),
		}

	def _createDirections( self ):
		self._directions = {
			Locators.Dynamic: self._getDynamicDetectorDirection,
		}
