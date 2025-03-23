from direct.gui.DirectButton import DirectButton

from entities.entityfactory import EntityFactory
from entities.parts.obstacles.cube import Cube
from entityloader import EntityLoader
from selector.selector import Selector


class EntityButtons:

	def __init__( self, selector: Selector, loader: EntityLoader, terrainSize, render ):

		self.__terrainSize = terrainSize
		self.__selector = selector
		self.__loader = loader
		self.create_entity_button()
		self.create_obstacle_button()
		self.__render = render

	def create_entity_button( self ):
		entityButton = DirectButton(
				text = "Entity",
				command = self.__createEntity,
				pos = (0, 0.7, 0.7),
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

	def __createEntity( self ):
		#tank = EntityFactory.create_entity( "basic_tank" )
		towerSmall = EntityFactory.create_entity( "tower_small" )
		entity = self.__loader.loadEntity( entity = towerSmall, entry = self.__selector.point )
		#entity.terrainSize = self.__terrainSize
		entity.__render = self.__render

	def __createObstacle( self ):
		cube = tank = EntityFactory.create_entity( "basic_tank" )
		entity = self.__loader.loadEntity( entity = cube, entry = self.__selector.point )
