from panda3d.core import Vec3

from entities.entity import Entity


class Entityphysics:
	@staticmethod
	def applyVelocity( entity: Entity,  velocity: Vec3 = Vec3( 500, 0, 0) ):
		if entity is None:
			return
		entity.rigidBodyNode.set_linear_velocity( velocity )

	@staticmethod
	def applyForce( entity: Entity,  force: Vec3 = Vec3( 100, 0, 0) ):
		if entity is None:
			return
		entity.rigidBodyNode.applyForce( force = force, pos = Vec3(0, 0, 0) )
