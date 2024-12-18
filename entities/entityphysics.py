from panda3d.core import Vec3

from entities.entity import Entity


class Entityphysics:

	@staticmethod
	def applyVelocity( entity: Entity, velocity: Vec3 = Vec3( 25, 0, 0 ) ):
		if entity is None:
			return
		entity.coreRigidBody.set_linear_velocity( velocity )

	@staticmethod
	def applyForce( entity: Entity, force: Vec3 = Vec3( 500, 500, 0 ) ):
		if entity is None:
			return
		next( iter( entity.rigidBodyNodes ) ).applyForce( force = force, pos = Vec3( 0, 0, 0 ) )

	def update_task( task, rigid_body ):
		# Reapply velocity in the task if needed
		rigid_body.setLinearVelocity( Vec3( 10, 0, 0 ) )
		return task.cont
