from panda3d.core import Vec4, Point3

from camera import TerrainCamera


class TerrainSelector:
    def __init__( self, terrainPicker, mouseWatcherNode, camNode, terrainCamera: TerrainCamera, render ):
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
        if custom_collision_polygon:
            if self.__last_custom_collision_polygon:
                self.__last_custom_collision_polygon.hideNeighbors()
            custom_collision_polygon.hideNeighbors()
            custom_collision_polygon.showNeighbors( custom_collision_polygon, custom_collision_polygon.row, custom_collision_polygon.col, 4 )
            custom_collision_polygon.showDebugNode()
            custom_collision_polygon.setColorDebugNode( Vec4( 0, 0, 0, 0.5 ) )
            self.__last_custom_collision_polygon = custom_collision_polygon
            self.__center = custom_collision_polygon.surfacePosition

    def on_map_hover( self ):
        entry = self.getNewEntry()
        if entry:
            print( 'update target' )
            point = entry.getSurfacePoint( self.__render )
            #rint( f"point: { point }",  )
            if ( point - self.__terrainCamera.center ).length() > 400:
                self.__terrainCamera.setCenter( point )
