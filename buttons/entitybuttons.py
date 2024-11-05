from direct.gui.DirectButton import DirectButton
from direct.task.Task import TaskManager

from entities.entityphysics import Entityphysics
from entities.full.movers.tank import Tank
from entities.modules.turret import CannonTurret
from entities.parts.engine import BasicEngine
from entities.parts.mobility import BasicTracks
from entityloader import EntityLoader
from selector.selector import Selector


class EntityButtons:

	def __init__( self, selector: Selector, loader: EntityLoader, taskMgr: TaskManager ):
		self.__selector = selector
		self.__loader = loader
		self.__taskMgr = taskMgr
		self.create_entity_button()
		self.create_velocity_button()

	def create_entity_button( self ):
		entityButton = DirectButton(
				text = "Entity",
				command = self.__createEntity,
				pos = (0, 0.7, 0.7),
				text_scale = 0.5,
				scale = 0.1
		)

	def create_velocity_button( self ):
		alignButton = DirectButton(
				text = "Velocity",
				command = self.__applyVelocity,
				pos = (0, -0.7, -0.7),
				text_scale = 0.5,
				scale = 0.1
		)

	def __applyVelocity( self ):
		try:
			self.__taskMgr.add( self.__selector.selectedEntity.track_target_angle, "track velocity", extraArgs = [ 90 ], appendTask = True )
			self.__taskMgr.add( self.__selector.selectedEntity.maintain_velocity, "track entity", extraArgs = [ 30 ], appendTask = True )
		except:
			pass

	def __createEntity( self ):
		engine = BasicEngine()
		turret = CannonTurret()
		mobility = BasicTracks()
		tank = Tank( engine = engine, turret = turret, mobility = mobility )
		self.__loader.loadEntity( entity = tank, entry = self.__selector.entry )
