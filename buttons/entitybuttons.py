from direct.gui.DirectButton import DirectButton

from entities.entityfactory import EntityFactory
from entities.parts.obstacles.cube import Cube
from entityloader import EntityLoader
from selector.selector import Selector


class EntityButtons:

	def __init__( self, selector: Selector, loader: EntityLoader ):
		self.__selector = selector
		self.__loader = loader
		self.create_tower_button()
		self.create_tank_button()
		self.create_obstacle_button()

	def create_tower_button( self ):
		entityButton = DirectButton(
				text = "Tower",
				command = self.__createTower,
				pos = (0, 0.7, 0.7),
				text_scale = 0.5,
				scale = 0.1
		)
	def create_tank_button( self ):
		entityButton = DirectButton(
				text = "Tank",
				command = self.__createTank,
				pos = (0, 0.9, 0.9),
				text_scale = 0.5,
				scale = 0.1
		)
	def create_obstacle_button( self ):
		obstacleButton = DirectButton(
				text = "Obstacle",
				command = self.__createObstacle,
				pos = (0, 0.4, 0.3),
				text_scale = 0.5,
				scale = 0.1
		)

	def __createTower( self ):
		towerSmall = EntityFactory.create_entity( "tower_small" )
		entity = self.__loader.loadEntity( entity = towerSmall, entry = self.__selector.point )

	def __createTank( self ):
		tank = EntityFactory.create_entity( "basic_tank" )
		entity = self.__loader.loadEntity( entity = tank, entry = self.__selector.point )

	def __createObstacle( self ):
		cube = tank = EntityFactory.create_entity( "cube" )
		entity = self.__loader.loadEntity( entity = cube, entry = self.__selector.point )
