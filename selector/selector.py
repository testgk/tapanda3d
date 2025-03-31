import queue

from camera.camera import TerrainCamera
from selection.selectionitem import SelectionItem
from selection.selectionmodes import SelectionModes


class Selector:
	def __init__( self, picker, mouseWatcherNode, camNode, terrainCamera: TerrainCamera, render ):
		self.__point = None
		self.__selectedItem: SelectionItem | None = None
		self.__entry = None
		self.__camNode = camNode
		self.__render = render
		self.__generalPicker = picker
		self.__mouseWatcherNode = mouseWatcherNode
		self.__terrainCamera = terrainCamera
		self.__selectionQueue = queue.Queue()
		self.__clearSelection = queue.Queue()
		self.__selectionMode = SelectionModes.NONE

	@property
	def point( self ):
		return self.__point

	def __getNewEntry( self ):
		if self.__mouseWatcherNode.hasMouse():
			mousePosition = self.__mouseWatcherNode.getMouse()
			return self.getEntry( mousePosition.getX(), mousePosition.getY() )

	def on_map_click( self, button: str = 'left' ):
		picked_item = self.__getPickedItem( button )
		if picked_item is None:
			self.__terrainCamera.clearSelectedItem()
			return
		if self.__selectedItem is None:
			self.__selectedItem = picked_item
			self.__selectedItem.handleSelection( SelectionModes.CREATE )
		else:
			self.__selectedItem = self.__selectedItem.selectItem( picked_item )
		self.__terrainCamera.setSelectedItem( self.__selectedItem )

	def __getPickedItem( self, button ):
		entry = self.__getNewEntry()
		self.__point = entry.getSurfacePoint( self.__render )
		print( f'point: {self.__point}' )
		self.__terrainCamera.setCenter( self.__point )
		if button == 'right':
			return None
		picked_obj = entry.getIntoNodePath()
		if picked_obj is None:
			return None
		print( f"Clicked node: { picked_obj }" )
		picked_item = picked_obj.node().getPythonTag( 'collision_target' )
		print( f"Clicked entity: { picked_item }" )
		return picked_item

	def getEntry( self, x, y ):
		self.__generalPicker.pickerRay.setFromLens( self.__camNode, x, y )
		self.__generalPicker.picker.traverse( self.__render )
		numEntries = self.__generalPicker.pickerQueue.getNumEntries()
		if numEntries > 0:
			self.__generalPicker.pickerQueue.sortEntries()
			entry = self.__generalPicker.pickerQueue.getEntry( 0 )
			return entry
