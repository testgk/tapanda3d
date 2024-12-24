from direct.gui.DirectButton import DirectButton
from direct.task.Task import TaskManager

from entities.full.movers.tank import Tank
from entities.modules.turret import CannonTurret
from entities.modules.chassis import BasicTracksChassis
from entities.obstacles.cube import Cube
from entities.parts.engine import BasicEngine
from entityloader import EntityLoader
from selector.selector import Selector


class EntityButtons:

	def __init__( self, selector: Selector, loader: EntityLoader, taskMgr: TaskManager, terrainSize ):

		self.__terrainSize = terrainSize
		self.__selector = selector
		self.__loader = loader
		self.__taskMgr = taskMgr
		self.create_entity_button()
		self.create_obstacle_button()

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
		engine = BasicEngine()
		turret = CannonTurret()
		chassis = BasicTracksChassis()
		tank = Tank( engine = engine, turret = turret, chassis = chassis )
		entity = self.__loader.loadEntity( entity = tank, entry = self.__selector.point )
		entity.terrainSize = self.__terrainSize

	def __createObstacle( self ):
		cube = Cube()
		entity = self.__loader.loadEntity( entity = cube, entry = self.__selector.point )
