from panda3d.core import Vec3

from entities.entity import Entity


class Entityphysics:


	@staticmethod
	def applyVelocity( entity: Entity,  velocity: Vec3 = Vec3( 50, 0, 0) ):
		if entity is None:
			return
		entity.rigidBodyNode.set_linear_velocity( velocity )
