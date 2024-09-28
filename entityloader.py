from panda3d.core import Vec3
from entities.entity import Entity


class EntityLoader:
	def __init__( self, render, physicsWorld ):
		self.__render = render
		self.physicsWorld = physicsWorld

	def loadEntity( self, entity: Entity, entry ):
		model_np = self.__render.attachNewNode( entity.rigidBodyNode )
		model_np.set_pos( entry.getSurfacePoint( self.__render ) )
		model_np.setZ( model_np.getZ() + 100 )
		entity.models[ 0 ].reparentTo( model_np )
		force = Vec3( 500, 0, 0 )  # Example force vector
		self.physicsWorld.attachRigidBody( entity.rigidBodyNode )
		entity.rigidBodyNode.applyForce( force, Vec3( 0, 0, 0 ) )
