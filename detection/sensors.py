from math import cos, radians, sin

from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import Vec3

from entities.locatorMode import Locators
from enums.colors import Color
from objects.spheres import createAndSetupSphere


class DetectorLimits:
	Wide = 120
	Normal = 45

class Senesors:
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
		self.__render = None
		self.__coreBodyPath = coreBodyPath

		self.__render = render
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
		return self.__detectors[ "edge" ].get_pos( self.__render )

	def __getLeftDetectorDirection( self ):
		leftPos = self.__detectors[ "left" ].get_pos( self.__render )
		edgePos = self.__detectors[ "leftEdge" ].get_pos( self.__render )
		return edgePos, leftPos

	def __getRightDetectorDirection( self ):
		rightPos = self.__detectors[ "right" ].get_pos( self.__render )
		edgePos = self.__detectors[ "rightEdge" ].get_pos( self.__render )
		return edgePos, rightPos

	def __getDynamicDetectorDirection( self ):
		dynamicPos = self.__detectors[ "dynamic" ].get_pos( self.__render )
		edgePos = self.__edgePos()
		return edgePos, dynamicPos

	def __createEdges( self ):
		taskMgr.add( self.moveDynamicDetector, "CircularMotionTask" )

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
		self.__detectors[ "dynamic" ].setPos( self._length / 2 + self._width * cos( radians_angle ),
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

	def __createDetector( self, color, position ):
		return createAndSetupSphere( self.__coreBodyPath, color, position )

	def edgePos( self ):
		return self.__detectors[ "edge" ].get_pos( self.__render )

	def getDirection( self, option ):
		return self.__directions[ option]()

	def _createDetectors( self ):
		self.__detectors = {
			"edge": self.__createDetector( Color.RED, Vec3( self._length / 2, 0, self._height ) ),
			"target": self.__createDetector( Color.ORANGE, Vec3( self._length, 0, self._height ) ),
			"leftEdge": self.__createDetector( Color.CYAN, Vec3( self._length / 2, self._width / 2, self._height ) ),
			"rightEdge": self.__createDetector( Color.CYAN, Vec3( self._length / 2, -self._width / 2, self._height ) ),
			"left": self.__createDetector( Color.RED, Vec3( self._length, self._width / 2, self._height ) ),
			"right": self.__createDetector( Color.BLUE, Vec3( self._length, -self._width / 2, self._height ) ),
			"dynamic": self.__createDetector( Color.YELLOW, Vec3( 0, 0, self._height ) ),
		}

	def _createDirections( self ):
		self.__directions = {
			Locators.Left: self.__getLeftDetectorDirection,
			Locators.Right: self.__getRightDetectorDirection,
			Locators.Dynamic: self.__getDynamicDetectorDirection,
		}
