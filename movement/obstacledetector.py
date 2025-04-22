import random

from panda3d.core import LineSegs, NodePath, Vec3

from detection.detector import Detector
from entities.locatorMode import Locators
from enums.colors import Color
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from entities.full.movers.mover import Mover


class ObstacleDetector:
	def __init__( self, entity, world, render ):
		self.__lastDetection = False
		self.__mover: Mover = entity
		self.__detector = Detector( entity, world, render )
		self.__detectedEntity = None

	@property
	def detectedEntity( self ):
		return self.__detectedEntity

	def detectObstacle( self, target ):
		if target is None:
			return None
		result, option = self.__detector.getDetection( target.position )
		if result.hasHits():
			for hit in result.getHits():
				hit_node = hit.getNode()
				if self.__mover.selfHit( hit_node ):
					continue
				try:
					item = hit_node.getPythonTag( 'raytest_target' )
				except AttributeError:
					continue
				if item is None:
					continue
				if not item.isObstacle:
					continue
				obstacle = item
				if self.__mover.selectedTarget( target ) and self.isCloser( self.__mover, target, obstacle ):
					continue
				if not self.isInbetween( self.__mover, obstacle, target ):
					continue
				obstacle.detection = option
				obstacle.handleSelection()
				return obstacle
		return None

	def detectAlternativePosition( self, target ):
		result, option = self.__detector.getDetection( locatorMode = Locators.Dynamic )
		if result.hasHits():
			for hit in result.getHits():
				hit_node = hit.getNode()
				if self.__mover.selfHit( hit_node ):
					continue
				try:
					item = hit_node.getPythonTag( 'raytest_target' )
				except AttributeError:
					continue
				if item is None:
					continue
				if not item.isTerrain:
					continue
				if not self.isCloser( target, item, self.__mover ):
					continue
				item.handleSelection()
				print( f'detected position: { item }' )
				return item
		return None

	def isCloser( self, origin, target1, target2 ):
		return ( origin.position - target1.position ).length() < ( origin.position - target2.position).length()

	def targetsDetection( self, task ):
		result, option = self.__detector.getDetection( locatorMode = Locators.Dynamic, lastDetection = self.__lastDetection  )
		self.__lastDetection = False
		if result.hasHits():
			for hit in result.getHits():
				hit_node = hit.getNode()
				try:
					item = hit_node.getPythonTag( 'raytest_target' )
				except AttributeError:
					continue
				if item is None or item.isTerrain:
					continue
				item.handleDetection()
				self.__lastDetection = True
				print( f'detected item: { item }' )
				self.__detectedEntity = item
				return task.again
		self.__detectedEntity = None
		return task.again

	def isInbetween( self, __mover, obstacle, target ):
		# Vectors from point B
		vec_ba = ( obstacle.position - self.__mover.position ).normalized()
		vec_bc = ( obstacle.position - target.position ).normalized()

		# Calculate the angle in degrees
		angle_deg = vec_ba.angle_deg( vec_bc )
		print( f'angle_deg: { angle_deg }' )
		return angle_deg > 120