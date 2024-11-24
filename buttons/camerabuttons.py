from direct.gui.DirectButton import DirectButton

from camera.camera import TerrainCamera


class CameraButtons:
    DEBUG = False
    def __init__( self, terrainCamera: TerrainCamera, debugNode ):
        self.__debugNode = debugNode
        self.camera = terrainCamera
        self.create_above_button()
        self.create_rotate_left_button()
        self.create_rotate_right_button()
        self.create_distance_view_button()
        self.create_zoom_in_button()
        self.create_zoom_out_button()
        self.create_debug_view_button()
        #self.create_zoom_center()

    def create_rotate_left_button( self ):
        rotate_button = DirectButton(
            text = "Left",
            command = self.camera.rotateCamera,
            pos = (0, 0, -0.9),
            text_scale = 0.5,
            scale = 0.1
        )

    def create_rotate_right_button( self ):
        rotate_button = DirectButton(
            text = "Right",
            command = self.camera.rotateCamera,
            pos = ( 0, 0, 0.9 ),
            scale = 0.1,
            text_scale = 0.5,
            extraArgs = [ -1 ]
        )

    def create_zoom_in_button( self ):
        zoom_in_button = DirectButton(
            text = "Zoom In",
            command = self.camera.zoomCamera,
            pos = ( -0.5, -0.9, 0 ),
            text_scale = 0.5,
            scale = 0.1,
            extraArgs = [ -100 ]
        )

    def create_zoom_center( self ):
        zoom_in_button = DirectButton(
            text = "Center",
            command = self.camera.zoomCenter,
            pos = ( -0.7, -0.7, 0 ),
            text_scale = 0.5,
            scale = 0.1,
            extraArgs = [ -100 ]
        )

    def create_zoom_out_button( self ):
        zoom_out_button = DirectButton(
            text = "Zoom Out",
            command = self.camera.zoomCamera,
            pos = ( 0.5, -0.9, 0 ),
            text_scale = 0.5,
            scale = 0.1,
            extraArgs = [ 100 ]
        )

    def create_above_button( self ) :
        rotate_button = DirectButton(
            text = "Hover",
            command = self.camera.hoverAbove,
            pos = ( 0.9, 0.9, 0 ),
            scale = 0.1,
            text_scale = 0.5,
        )

    def create_distance_view_button( self ):
        rotate_button = DirectButton(
            text = "Distance",
            command = self.camera.hoverDistance,
            pos = ( -0.9, -0.9, 0 ),
            text_scale = 0.5,
            scale = 0.1
        )

    def create_debug_view_button( self ):
        debug_button = DirectButton(
            text = "Debug",
            command = self.__debugMode,
            pos = ( -0.7, 0.7, 0 ),
            text_scale = 0.5,
            scale = 0.1
        )

    def __debugMode( self ):
       if self.DEBUG:
           self.__debugNode.hide()
           self.DEBUG = False
       else:
           self.__debugNode.show()
           self.DEBUG = True
           
