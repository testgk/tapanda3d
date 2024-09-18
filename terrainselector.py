from panda3d.bullet import BulletHelper, BulletRigidBodyNode, BulletTriangleMesh, BulletTriangleMeshShape
from panda3d.core import Vec4 ,BitMask32

from camera import TerrainCamera
import customcollisionpolygon
from direct.showbase.ShowBase import ShowBase

from enums.colors import Color
from phyisics import globalClock


class TerrainSelector:
    def __init__( self, terrain, terrainPicker, mouseWatcherNode, camNode, terrainCamera: TerrainCamera, physicsWorld, taskMgr, render ):
        self.__terrain = terrain
        self.taskMgr = taskMgr
        self.__last_custom_collision_polygon = None
        self.__camNode = camNode
        self.__render = render
        self.__terrainPicker = terrainPicker
        self.__mouseWatcherNode = mouseWatcherNode
        self.__terrainCamera = terrainCamera
        self.physicsWorld = physicsWorld

    def getNewEntry( self ):
        if self.__mouseWatcherNode.hasMouse():
            mousePosition = self.__mouseWatcherNode.getMouse()
            self.__terrainPicker.pickerRay.setFromLens( self.__camNode, mousePosition.getX(), mousePosition.getY() )
            self.__terrainPicker.picker.traverse( self.__render )
            numEntries = self.__terrainPicker.pickerQueue.getNumEntries()
            if numEntries > 0:
                self.__terrainPicker.pickerQueue.sortEntries()
                entry = self.__terrainPicker.pickerQueue.getEntry( 0 )
                return entry

    def on_map_click( self ):
        entry = self.getNewEntry()
        if entry:
            #print( 'update target' )
            point = entry.getSurfacePoint( self.__render )
            print( f"point: { point }")
            self.__terrainCamera.setCenter( point )

    def markArea( self ):
        entry = self.getNewEntry()
        if entry is None:
            return
        picked_obj = entry.getIntoNodePath()
        print( f"Clicked node: { picked_obj }" )
        custom_collision_polygon = picked_obj.node().getPythonTag( 'custom_collision_polygon' )
        custom_collision_polygon.removeAllEdges()
        if custom_collision_polygon:
            if self.__last_custom_collision_polygon:
                self.__last_custom_collision_polygon.hideNeighbors()
            customcollisionpolygon.currentFrame.clear()
            custom_collision_polygon.hideNeighbors()
            custom_collision_polygon.showNeighbors( custom_collision_polygon.row, custom_collision_polygon.col, 4 )
            custom_collision_polygon.showDebugNode()
            custom_collision_polygon.colorDebugNode( Vec4( 0, 0, 0, 0.5 ) )
            print( f' height {custom_collision_polygon.terrainPosition[2] }')
            self.__last_custom_collision_polygon = custom_collision_polygon


    def on_map_loader_click( self, model ):
        entry = self.getNewEntry()
        if entry is None:
            return
        picked_obj = entry.getIntoNodePath()
        print( f"Clicked node: { picked_obj }" )
        custom_collision_polygon = picked_obj.node().getPythonTag( 'custom_collision_polygon' )
        if custom_collision_polygon:
            custom_collision_polygon.showDebugNode()
            #model.setScale( 0.2 )
            #model.reparentTo( self.__render )
            #model.set_pos( entry.getSurfacePoint( self.__render ) )
            #model.setZ( model.getZ() + 1 )

            # Create a BulletTriangleMesh
            mesh = BulletTriangleMesh()
            # Add the geometry of the model to the triangle mesh
            self.add_model_to_bullet_mesh( mesh, model )

            # Create a BulletTriangleMeshShape from the mesh
            model_shape = BulletTriangleMeshShape( mesh, dynamic = True )  # dynamic=True for movable objects

            # Create a BulletRigidBodyNode for the model and attach the shape
            model_node = BulletRigidBodyNode( 'Model' )
            model_node.addShape( model_shape )
            model_node.setMass( 1.0 )  # Dynamic body (affected by gravity)
            model_np = self.__render.attachNewNode( model_node )
            model_np.set_pos( entry.getSurfacePoint( self.__render ) )
            model.reparentTo( model_np )
            self.physicsWorld.attachRigidBody( model_node )
            self.taskMgr.add( self.update_physics, "update_physics" )

            #model.setColor( Color.GREEN.value )
    def update_physics(self, task):
        """Update the physics world."""
        dt = globalClock.getDt()
        self.physicsWorld.doPhysics(dt)
        return task.cont

    def on_map_hover( self ):
        entry = self.getNewEntry()
        if entry:
            #print( 'update target' )
            point = entry.getSurfacePoint( self.__render )
            distance =  ( self.__terrainCamera.center - point ).length()
            if distance < 400:
                return
            print( f'length: {distance}' )
            center = ( point + self.__terrainCamera.center ) / 2
            self.__terrainCamera.setCenter( center )


    def create_model_physics( self, model ) :
        mesh = BulletTriangleMesh()
        BulletHelper.fromCollisionSolids( mesh, model.node() )
        shape = BulletTriangleMeshShape( mesh, dynamic = True )  # Set dynamic=True for non-static
        return shape


    def add_model_to_bullet_mesh(self, mesh, model_np):
        """Adds the geometry of the model to a BulletTriangleMesh."""
        geom_node = model_np.find("**/+GeomNode").node()

        for i in range(geom_node.getNumGeoms()):
            geom = geom_node.getGeom(i)
            mesh.addGeom(geom)


