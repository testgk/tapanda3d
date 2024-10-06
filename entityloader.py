from panda3d.core import Vec3
from entities.entity import Entity


class EntityLoader:
	def __init__( self, render, physicsWorld, loader ):
		self.__render = render
		self.__physicsWorld = physicsWorld
		self.__loader = loader

	def loadEntity( self, entity: Entity, entry ):
		entity.buildModels( loader = self.__loader )
		model_np = self.__render.attachNewNode( entity.rigidBodyNode )
		self.__physicsWorld.attachRigidBody( entity.rigidBodyNode )
		model_np.set_pos( entry.getSurfacePoint( self.__render ) )
		model_np.setZ( model_np.getZ() + 50 )
		for models in entity.models:
			models.reparentTo( model_np )
