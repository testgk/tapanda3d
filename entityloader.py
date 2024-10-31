from direct.task.Task import TaskManager
from panda3d.bullet import BulletConstraint, BulletGenericConstraint, BulletHingeConstraint, BulletSliderConstraint
from panda3d.core import BitMask32, LPoint3, LVector3, Point3, TransformState, Vec3

from collsiongroups import CollisionGroup
from entities.entity import Entity
from entities.mover import Mover


class EntityLoader:
	def __init__( self, render, physicsWorld, loader, taskMgr: TaskManager ):
		self.__render = render
		self.__physicsWorld = physicsWorld
		self.__loader = loader
		self.__taskMgr = taskMgr

	def loadEntity( self, entity: Mover, entry ):
		entity.buildModels( loader = self.__loader )
		nps = [ ]
		for rigidGroup, rm in entity.rigidBodyNodes.items():
			modelBulletNodePath = self.__renderModelsGroup( entry, rm[ "models" ], rm[ "rb" ] )
			if entity.isRigidGroup( rigidGroup ):
				entity.setCoreBody( modelBulletNodePath,  rm[ "rb" ] )
		self.__taskMgr.add( entity.track_target_angle, "track entity", extraArgs=[ 60 ], appendTask = True )


	def __renderModelsGroup( self, entry, models, bulletNode ):
		modelBullet = self.__render.attachNewNode( bulletNode )
		self.__physicsWorld.attachRigidBody( bulletNode )
		modelBullet.set_pos( entry.getSurfacePoint( self.__render ) )
		modelBullet.setZ( modelBullet.getZ() + 50  )
		for model in models:
			model.reparentTo( modelBullet )
		return modelBullet

	def track_entity( self, entity: Mover, task ):
		entity.track_target_angle( -120, task )
