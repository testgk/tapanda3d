

class Selector:
    def __init__(self, terrainPicker, mouseWatcherNode ):
        self.__terrainPicker = terrainPicker
        self.__mouseWatcherNode = mouseWatcherNode

    def on_map_click( self ):
        if self.__mouseWatcherNode.hasMouse():
            mousePosition = self.__mouseWatcherNode.getMouse()

            # Set the position of the ray based on the mouse position
            self.__terrainPicker.pickerRay.setFromLens( self.camNode, mousePosition.getX(), mousePosition.getY() )

            # Perform the collision detection
            self.__terrainPicker.picker.traverse( self.__render )

            print( f"Mouse position: { mousePosition }" )  # Debugging
            print( f"Traversing collisions..." )  # Debugging

            numEntries = self.__terrainPicker.pickerQueue.getNumEntries()
            print( f"Number of collision entries: {numEntries}" )  # Debugging

            if numEntries > 0:
                # Sort entries so the closest is first
                self.__terrainPicker.pickerQueue.sortEntries()
                entry = self.__terrainPicker.pickerQueue.getEntry( 0 )
                point = entry.getSurfacePoint( self.__render )

                print( f"Collision detected at: { point }" )
                picked_obj = entry.getIntoNodePath()
                print( f"Clicked node: { picked_obj }" )
                custom_collision_polygon = picked_obj.node().getPythonTag( 'custom_collision_polygon' )
                if custom_collision_polygon:
                    print( f"CustomCollisionPolygon instance: { custom_collision_polygon }" )
                    # Access the parent class attributes or methods as needed
                    print( f"Parent node: { custom_collision_polygon.name }" )
                    custom_collision_polygon.showDebugNode()
                    custom_collision_polygon.hideNeighbors()
                    custom_collision_polygon.showNeighbors( custom_collision_polygon.row, custom_collision_polygon.col, 1 )
                # Update the terrain __center to the clicked point

                self.__center = point
                self.__cameraRadius = self.CLOSE_PROXIMITY
                self.__updateCameraPosition()
            else:
                print( "No collisions detected." )  # Debugging