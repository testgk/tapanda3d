from direct.task.Task import TaskManager
from panda3d.core import Loader, TransparencyAttrib

from entities.entity import Entity
from entities.full.movers.mover import Mover


class EntityLoader:
	def __init__( self, render, physicsWorld, loader: Loader, terrainSize ):
		self.__render = render
		self.__physicsWorld = physicsWorld
		self.__loader = loader
		self.__terrainSize = terrainSize

	def loadEntity( self, entity: Entity, entry ):
		entity.buildModels( loader = self.__loader )
		for rigidGroup, rm in entity.rigidBodyNodes.items():
			parts = rm[ "parts" ]
			bulletNode = rm[ "rigidbody" ]
			self.__renderModelsGroup( point = entry, parts = parts,  bulletNode = bulletNode )
		entity.completeLoading( self.__physicsWorld, self.__render, self.__terrainSize )
		return entity

	def __renderModelsGroup( self, point, parts, bulletNode ):
		modelBullet = self.__render.attachNewNode( bulletNode )
		self.__physicsWorld.attachRigidBody( bulletNode )
		modelBullet.set_pos( point )
		modelBullet.setZ( modelBullet.getZ() + 100  )
		for part in parts:
			part.rigidBodyPath = modelBullet
			part.model.reparentTo( modelBullet )
			if part.pseudoPart:
				part.model.setTransparency( TransparencyAttrib.M_alpha )
				part.model.setBin( "transparent", 0 )
				part.model.hide()
		return modelBullet
