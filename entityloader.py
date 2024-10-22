from panda3d.bullet import BulletConstraint, BulletGenericConstraint, BulletHingeConstraint, BulletSliderConstraint
from panda3d.core import BitMask32, LPoint3, LVector3, Point3, TransformState, Vec3

from collsiongroups import CollisionGroup
from entities.entity import Entity


class EntityLoader:
	def __init__( self, render, physicsWorld, loader ):
		self.__render = render
		self.__physicsWorld = physicsWorld
		self.__loader = loader

	def loadEntity( self, entity: Entity, entry ):
		entity.buildModels( loader = self.__loader )
		nps = [ ]
		for bulletNode, models in entity.rigidBodyNodes.items():
			nps.append( self.__renderModelsGroup( entry, models, bulletNode ) )

	def __renderModelsGroup( self, entry, models, bulletNode ):
		modelBullet = self.__render.attachNewNode( bulletNode )
		self.__physicsWorld.attachRigidBody( bulletNode )
		modelBullet.set_pos( entry.getSurfacePoint( self.__render ) )
		modelBullet.setZ( modelBullet.getZ() + 50  )
		for model in models:
			model.reparentTo( modelBullet )
		return modelBullet
