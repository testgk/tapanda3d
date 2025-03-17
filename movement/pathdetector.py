import random

from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import ClockObject, LineSegs, NodePath, Vec3

from customcollisionpolygon import CustomCollisionPolygon
from custompolygon import CustomPolygon
from customrigidpolygon import CustomRigidPolygon
from entities.locatorMode import Locators
from enums.colors import Color
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from entities.full.movers.mover import Mover


class PathDetector:
	def __init__( self, entity, world, render ):
		self.__mover: Mover = entity
		self.__world = world
		self.__ray = None
		self.__render = render

	def detectObstacle( self, target ):
		if target is None:
			return None
		result, option = self.__getDetection( target.position )
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
				obstacle.detection = option
				obstacle.handleSelection()
				return obstacle
		return None

	def detectAlternativePosition( self, target ):
		result, option = self.__getDetection( locatorMode = Locators.Dynamic )
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
				print( f'detect position: { item }' )
				return item
		return None

	def __getDetection( self, target = None, locatorMode: Locators = None ):
		global edge
		if self.__ray:
			self.__ray.remove_node()
		if self.__mover.locatorMode == Locators.NONE:
			return None
		option = locatorMode or random.choice( self.__mover.locatorMode.value )
		if option == Locators.Target:
			edge = self.__mover.edgePos()
			detector = target
			detector.z = edge.getZ()
		else:
			edge, detector = self.__mover.getDetector( option )
		direction = Vec3( detector - edge )
		self.__ray = self.visualize_ray( start = edge, color = Color.GREEN, end = edge + direction * self.__mover.detectorLength )
		result = self.__world.rayTestAll( edge, edge + direction * 10 )
		return result, option

	def visualize_ray( self, start, end, color = Color.GREEN, thickness = 2.0 ):
		if self.__mover.hasObstacles():
			color = Color.RED
		color = color
		line = LineSegs()
		line.set_thickness( thickness )
		line.set_color( *color )  # RGBA
		line.move_to( start )
		line.draw_to( end )
		line_node = NodePath( line.create() )
		line_node.reparent_to( self.__render )
		return line_node

	def isCloser( self, origin, target1, target2 ):
		return ( origin.position - target1.position ).length() < ( origin.position - target2.position).length()
