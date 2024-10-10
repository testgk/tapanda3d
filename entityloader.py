from panda3d.core import Vec3
from entities.entity import Entity


class EntityLoader:
	def __init__( self, render, physicsWorld, loader ):
		self.__render = render
		self.__physicsWorld = physicsWorld
		self.__loader = loader

	def loadEntity( self, entity: Entity, entry ):
		entity.buildModels( loader = self.__loader )
		for node in entity.rigidBodyNode:
			model = node.getPythonTag( 'body_node' )
			model_np = self.__render.attachNewNode( node )
			self.__physicsWorld.attachRigidBody( node )
			model_np.set_pos( entry.getSurfacePoint( self.__render ) )
			model_np.setZ( model_np.getZ() + 50 )
			model.reparentTo( model_np )

		#for models in entity.models:
		#	models.reparentTo( model_np )
