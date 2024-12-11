from direct.task.Task import TaskManager
from panda3d.core import Loader

from entities.full.movers.mover import Mover


class EntityLoader:
	def __init__( self, render, physicsWorld, loader: Loader, taskMgr: TaskManager ):
		self.__render = render
		self.__physicsWorld = physicsWorld
		self.__loader = loader
		self.__taskMgr = taskMgr

	def loadEntity( self, entity: Mover, entry ):
		entity.buildModels( loader = self.__loader )
		for rigidGroup, rm in entity.rigidBodyNodes.items():
			parts = rm[ "parts" ]
			bulletNode = rm[ "rigidbody" ]
			self.__renderModelsGroup( point = entry, parts = parts,  bulletNode = bulletNode )
		entity.setDamping()
		entity.connectModules( self.__physicsWorld )
		return entity

	def __renderModelsGroup( self, point, parts, bulletNode ):
		modelBullet = self.__render.attachNewNode( bulletNode )
		self.__physicsWorld.attachRigidBody( bulletNode )
		modelBullet.set_pos( point )
		modelBullet.setZ( modelBullet.getZ() + 50  )
		for part in parts:
			part.rigidBodyPath = modelBullet
			part.model.reparentTo( modelBullet )
		return modelBullet
