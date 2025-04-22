import random
from collections import deque

from panda3d.core import LineSegs, NodePath, Vec3

from entities.locatorMode import Locators
from enums.colors import Color


class Detector:

	def __init__( self, entity, world, render ):
		self.__rayColor = Color.GREEN
		self.__lastLocatorMode = None
		self.__rays = deque()
		self.__render = render
		self.__world = world
		self.__entity = entity
		self.__ray = None
		self.__locatorNumbers = {
			Locators.NONE: 0,
			Locators.Right: 1,
			Locators.Left: 1,
			Locators.Target: 2,
			Locators.Dynamic: 10,
		}

	def getDetection( self, target = None, locatorMode: Locators = None ):
		global edge
		if len( self.__rays ) > 5:
			self.__rays.popleft().remove_node()
		if self.__entity.locatorMode == Locators.NONE:
			return None
		option = locatorMode or random.choice( self.__entity.locatorMode.value )
		if locatorMode != self.__lastLocatorMode:
			self.__clearRays()
			self.__lastLocatorMode = locatorMode
		if option == Locators.Target:
			edge = self.__entity.sensors.edgePos()
			detector = target
			detector.z = edge.getZ()
		else:
			edge, detector = self.__entity.sensors.getDirection( option )
		direction = Vec3( detector - edge )
		self.__rays.append( self.__visualize_ray( start = edge, color =  self.__rayColor,
											end = edge + direction * self.__entity.detectorLength ) )
		result = self.__world.rayTestAll( edge, edge + direction * 10 )
		return result, option

	def __clearRays( self ):
		while any( self.__rays ):
			self.__rays.popleft().remove_node()

	def detectionTask( self, task ):
		global edge
		if len( self.__rays ) > 10:
			self.__rays.popleft().remove_node()
		edge, detector = self.__entity.sensors.getDirection( Locators.Dynamic )
		direction = Vec3( detector - edge )
		result = self.__world.rayTestAll( edge, edge + direction * 10 )
		if self.__entity.isSelected():
			self.__rays.append( self.__visualize_ray( start = edge, color = self.__rayColor,
												end = edge + direction * self.__entity.detectorLength ) )
		else:
			self.__clearRays()
		self.__entity.analyzeDetection( result )
		return task.cont

	def __visualize_ray( self, start, end, color = Color.GREEN, thickness = 2.0 ):
		color = self.__entity.detectorColor() or color
		line = LineSegs()
		line.set_thickness( thickness )
		line.set_color( *color )  # RGBA
		line.move_to( start )
		line.draw_to( end )
		line_node = NodePath( line.create() )
		line_node.reparent_to( self.__render )
		return line_node

	def setColor( self, color ):
		self.__rayColor = color
