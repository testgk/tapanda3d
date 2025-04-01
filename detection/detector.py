import random

from panda3d.core import LineSegs, NodePath, Vec3

from entities.locatorMode import Locators
from enums.colors import Color


class Detector( object ):

	def __init__( self, entity, world, render ):
		self.__render = render
		self.__world = world
		self.__entity = entity
		self.__ray = None

	def getDetection( self, target = None, locatorMode: Locators = None ):
		global edge
		if self.__ray:
			self.__ray.remove_node()
		if self.__entity.locatorMode == Locators.NONE:
			return None
		option = locatorMode or random.choice( self.__entity.locatorMode.value )
		if option == Locators.Target:
			edge = self.__entity.sensors.edgePos()
			detector = target
			detector.z = edge.getZ()
		else:
			edge, detector = self.__entity.sensors.getDirection( option )
		direction = Vec3( detector - edge )
		self.__ray = self.__visualize_ray( start = edge, color = Color.GREEN,
											end = edge + direction * self.__entity.detectorLength )
		result = self.__world.rayTestAll( edge, edge + direction * 10 )
		return result, option

	def detectionTask( self, task ):
		global edge
		if self.__ray:
			self.__ray.remove_node()
		edge, detector = self.__entity.sensors.getDirection( Locators.Dynamic )
		direction = Vec3( detector - edge )
		self.__ray = self.__visualize_ray( start = edge, color = Color.GREEN,
											end = edge + direction * self.__entity.detectorLength )
		result = self.__world.rayTestAll( edge, edge + direction * 10 )
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
