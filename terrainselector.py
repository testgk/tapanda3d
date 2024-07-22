

from panda3d.core import Vec4

from camera import TerrainCamera
import customcollisionpolygon
from direct.showbase.ShowBase import ShowBase

from enums.colors import Color


class TerrainSelector:
    def __init__( self, terrain, terrainPicker, mouseWatcherNode, camNode, terrainCamera: TerrainCamera, render ):
        self.__terrain = terrain
        self.__last_custom_collision_polygon = None
        self.__camNode = camNode
        self.__render = render
        self.__terrainPicker = terrainPicker
        self.__mouseWatcherNode = mouseWatcherNode
        self.__terrainCamera = terrainCamera

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
            #custom_collision_polygon.showDebugNode()
            model.setScale( 0.5 )
            model.reparentTo( self.__render )
            model.set_pos( custom_collision_polygon.terrainPosition )
            model.setZ( model.getZ() + 5 )
            #model.setColor( Color.GREEN.value )

    def on_map_hover( self ):
        entry = self.getNewEntry()
        if entry:
            #print( 'update target' )
            point = entry.getSurfacePoint( self.__render )
            #rint( f"point: { point }",  )
            if ( point - self.__terrainCamera.center ).length() > 400:
                self.__terrainCamera.setCenter( point )
