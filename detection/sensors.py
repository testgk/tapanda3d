from math import cos, radians, sin

from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import Vec3

from detection.towersensors import TowerSensors
from entities.locatorMode import Locators
from enums.colors import Color
from objects.spheres import createAndSetupSphere


class DetectorLimits:
	Wide = 120
	Normal = 45

class Senesors( TowerSensors ):
	def __init__( self, coreBodyPath, length, width, height, render  ):
		super().__init__( coreBodyPath, length, width, height, render )

	def __edgePos( self ):
		return self._detectors[ "edge" ].get_pos( self._render )

	def __getLeftDetectorDirection( self ):
		leftPos = self._detectors[ "left" ].get_pos( self._render )
		edgePos = self._detectors[ "leftEdge" ].get_pos( self._render )
		return edgePos, leftPos

	def __getRightDetectorDirection( self ):
		rightPos = self._detectors[ "right" ].get_pos( self._render )
		edgePos = self._detectors[ "rightEdge" ].get_pos( self._render )
		return edgePos, rightPos

	def __createEdges( self ):
		taskMgr.add( self.moveDynamicDetector, "CircularMotionTask" )

	def _createDetectors( self ):
		self._detectors = {
			"edge": self._createDetector( Color.RED, Vec3( self._length / 2, 0, self._height ) ),
			"target": self._createDetector( Color.ORANGE, Vec3( self._length, 0, self._height ) ),
			"leftEdge": self._createDetector( Color.CYAN, Vec3( self._length / 2, self._width / 2, self._height ) ),
			"rightEdge": self._createDetector( Color.CYAN, Vec3( self._length / 2, -self._width / 2, self._height ) ),
			"left": self._createDetector( Color.RED, Vec3( self._length, self._width / 2, self._height ) ),
			"right": self._createDetector( Color.BLUE, Vec3( self._length, -self._width / 2, self._height ) ),
			"dynamic": self._createDetector( Color.YELLOW, Vec3( 0, 0, self._height ) ),
		}

	def _createDirections( self ):
		self._directions = {
			Locators.Left: self.__getLeftDetectorDirection,
			Locators.Right: self.__getRightDetectorDirection,
			Locators.Dynamic: self._getDynamicDetectorDirection,
		}
