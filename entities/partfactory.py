import os
from collections import defaultdict
from typing import TYPE_CHECKING, Callable

from panda3d.bullet import BulletRigidBodyNode, BulletTriangleMesh, BulletTriangleMeshShape
from panda3d.core import BitMask32, CollisionBox, CollisionHandlerPusher, CollisionNode, CollisionTraverser, NodePath, \
	Vec3
from panda3d.core import Vec3, CollisionBox, CollisionNode


from collsiongroups import CollisionGroup

if TYPE_CHECKING:
	from entities.entity import Entity
	from entities.parts.part import Part

from objects.stltoeggconverter import convert_stl_to_egg


def find_entity_parts( cls ) -> tuple[ list[ Callable ], list[ Callable ] ]:
	entityParts = [ ]
	entityModules = [ ]
	for name in dir( cls ):
		attr = getattr( cls, name )
		if getattr( attr, '_is_entitypart', False ):
			entityParts.append( attr )
		elif getattr( attr, '_is_entitymodule', False ):
			entityModules.append( attr )
	return entityParts, entityModules


class PartFactory:
	def __init__( self, entity: 'Entity' ):
		self.partModels = { }
		self.__modules = [ ]
		self.__parts = [ ]
		self.__entity = entity

	def addParts( self ):
		parts, modules = find_entity_parts( self.__entity )
		for part in parts:
			self.__parts.append( part() )
		for module in modules:
			self.__modules.append( module() )
		return self.__parts, self.__modules

	@property
	def collisionSystems( self ):
		return self.__collision_nps

	@property
	def models( self ):
		return self.__models

	@property
	def rigidBodies( self ):
		return self.__rigidBodies

	def build( self, loader ):
		self.addParts()
		self.createModels( loader )
		self.createCollisionSystem()
		self.createRigidBodies()

	def createModels( self, loader ) -> None:
		self.__models = []
		for part in self.__parts:
			if not part.isRendered:
				continue
			try:
				eggPath = self.__getPartEggPath( part )
				model = self.__loadModel( eggPath, loader, part )
				self.partModels[ part ] = model
				self.__models.append( model )
			except Exception as e:
				pass

	def __loadModel( self, eggPath, loader, part ):
		model = loader.loadModel( eggPath )
		model.setScale( 1 )
		model.setColor( part.color )
		model.setPythonTag( 'model_part', part )
		return model

	def __getPartEggPath( self, part: 'Part' ):
		fullPath = os.path.join( "objects/parts/", part.objectPath, part.partId )
		eggPath = fullPath + ".egg"
		if os.path.exists( eggPath ):
			return eggPath
		else:
			stlPath = fullPath + ".stl"
			if os.path.exists( stlPath ):
				convert_stl_to_egg( stlPath, eggPath )
				return eggPath

	def createCollisionSystem( self ):
		self.__collision_nps = [ ]
		for part, model in self.partModels.items():
			if model is None:
				return
			collision_box_node = create_collision_box( model )
			if collision_box_node:
				collision_np = model.attachNewNode( collision_box_node )
				self.__collision_nps.append( collision_np )

	def createRigidBodies( self ) -> None:
		self.__rigidBodies = {}
		groupedPartModels = defaultdict( list )
		for part, model in self.partModels.items():
			groupedPartModels[ part.rigidGroup ].append( model )

		for rg, models in groupedPartModels.items():
			part = models[ 0 ].getPythonTag( 'model_part' )
			body_node = self.__createRigidBody( models )
			if hasattr( part, 'friction' ):
				body_node.setFriction( part.friction )
			body_node.setIntoCollideMask( BitMask32.allOff() )
			body_node.setIntoCollideMask(  part.collideGroup )
			self.__rigidBodies[ body_node ] = models

	def __createRigidBody( self, models: list ) -> BulletRigidBodyNode:
		body_node = BulletRigidBodyNode( 'multi_shape_body' )
		for model in models:
			mesh = BulletTriangleMesh()
			add_model_to_bullet_mesh( mesh, model )
			model_shape = BulletTriangleMeshShape( mesh, dynamic = True )
			body_node.addShape( model_shape )
			body_node.setMass( 100 )
			#body_node.setPythonTag( 'body_node', model )
		return body_node


def get_model_dimensions( model_np ):
	"""Gets the approximate dimensions of a model."""
	geom_node = model_np.find( "**/+GeomNode" ).node()
	if not geom_node:
		return None

	# Initialize min and max bounds with large values to ensure they are updated
	min_bounds = Vec3( float( 'inf' ), float( 'inf' ), float( 'inf' ) )
	max_bounds = Vec3( float( '-inf' ), float( '-inf' ), float( '-inf' ) )

	# Loop over all geometries in the node to compute the bounds
	for i in range( geom_node.getNumGeoms() ):
		geom = geom_node.getGeom( i )
		bounds = geom.getBounds()

		# Update min_bounds
		min_bounds.setX( min( min_bounds.x, bounds.getMin().x ) )
		min_bounds.setY( min( min_bounds.y, bounds.getMin().y ) )
		min_bounds.setZ( min( min_bounds.z, bounds.getMin().z ) )

		# Update max_bounds
		max_bounds.setX( max( max_bounds.x, bounds.getMax().x ) )
		max_bounds.setY( max( max_bounds.y, bounds.getMax().y ) )
		max_bounds.setZ( max( max_bounds.z, bounds.getMax().z ) )

	return min_bounds, max_bounds

def create_collision_box( model_np ):
	"""Creates a CollisionBox that roughly matches the model's dimensions."""
	dimensions = get_model_dimensions( model_np )
	if dimensions is None:
		return None

	min_bounds, max_bounds = dimensions

	# Calculate width, height, and depth
	width = max_bounds.x - min_bounds.x
	height = max_bounds.y - min_bounds.y
	depth = max_bounds.z - min_bounds.z

	# Calculate the center of the box
	center_x = (min_bounds.x + max_bounds.x) / 2
	center_y = (min_bounds.y + max_bounds.y) / 2
	center_z = (min_bounds.z + max_bounds.z) / 2

	# Create a CollisionBox with the center and half extents (width / 2, height / 2, depth / 2)
	collision_box = CollisionBox(
			Vec3( center_x, center_y, center_z ),  # Center of the box
			width / 2, height / 2, depth / 2  # Half extents (dimensions divided by 2)
	)

	# Create a collision node to attach the collision box to
	collision_node = CollisionNode( 'model_collision' )
	collision_node.addSolid( collision_box )
	return collision_node

def add_model_to_bullet_mesh( mesh, model_np ):
	"""Adds the geometry of the model to a BulletTriangleMesh."""
	geom_node = model_np.find( "**/+GeomNode" ).node()
	for i in range( geom_node.getNumGeoms() ):
		geom = geom_node.getGeom( i )
		mesh.addGeom( geom )
