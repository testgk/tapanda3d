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
			modelBulletNodePath = self.__renderModelsGroup( point = entry, models = rm[ "models" ],  bulletNode = rm[ "rigidbody" ] )
			if entity.isCoreBodyRigidGroup( rigidGroup ):
				entity.setCoreBody( modelBulletNodePath,  rm[ "rigidbody" ] )
				entity.coreRigidBody.set_linear_damping( 0 )
				entity.coreRigidBody.set_angular_damping( 0 )
		entity.reparentModels()
		return entity

	def __renderModelsGroup( self, point, models, bulletNode ):
		modelBullet = self.__render.attachNewNode( bulletNode )
		self.__physicsWorld.attachRigidBody( bulletNode )
		modelBullet.set_pos( point )
		modelBullet.setZ( modelBullet.getZ() + 50  )
		for model in models:
			model.reparentTo( modelBullet )
		return modelBullet
