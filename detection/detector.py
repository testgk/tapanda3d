import random
from collections import deque

from panda3d.core import LineSegs, NodePath, Vec3

from entities.locatorMode import Locators
from enums.colors import Color


class Detector( object ):

	def __init__( self, entity, world, render ):
		self.__lastLocatorMode = None
		self.__rays = deque()
		self.__render = render
		self.__world = world
		self.__entity = entity
		self.__ray = None

	def getDetection( self, target = None, locatorMode: Locators = None ):
		global edge
		if len( self.__rays ) > 10:
			self.__rays.popleft().remove_node()
		if self.__entity.locatorMode == Locators.NONE:
			return None
		option = locatorMode or random.choice( self.__entity.locatorMode.value )
		if locatorMode != self.__lastLocatorMode:
			self.__clearRays()
		if option == Locators.Target:
			edge = self.__entity.sensors.edgePos()
			detector = target
			detector.z = edge.getZ()
		else:
			edge, detector = self.__entity.sensors.getDirection( option )
		direction = Vec3( detector - edge )
		self.__rays.append( self.__visualize_ray( start = edge, color = Color.GREEN,
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
			self.__rays.append( self.__visualize_ray( start = edge, color = Color.GREEN,
												end = edge + direction * self.__entity.detectorLength ) )
		else:
			self.__clearRays()
		return task.cont


	def __visualize_ray( self, start, end, color = Color.GREEN, thickness = 2.0 ):
		#if self.__entity.hasObstacles():
		#	color = Color.RED
		color = self.__entity.detectorColor() or color
		line = LineSegs()
		line.set_thickness( thickness )
		line.set_color( *color )  # RGBA
		line.move_to( start )
		line.draw_to( end )
		line_node = NodePath( line.create() )
		line_node.reparent_to( self.__render )
		return line_node
