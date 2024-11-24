import queue

from camera.camera import TerrainCamera
from entities.full.movers.mover import Mover
from selectionmodes import SelectionModes


class Selector:
	def __init__( self, picker, mouseWatcherNode, camNode, terrainCamera: TerrainCamera, render ):
		self.__entry = None
		self.__camNode = camNode
		self.__render = render
		self.__generalPicker = picker
		self.__mouseWatcherNode = mouseWatcherNode
		self.__terrainCamera = terrainCamera
		self.__selectionQueue = queue.Queue()
		self.__clearSelection = queue.Queue()
		self.__selectionMode = SelectionModes.NONE
		self.__selectionHandlers = {
				SelectionModes.CREATE: self.__createSelection,
				SelectionModes.P2P: self.__p2pSelection
		}
		self.__selectedMover = None

	@property
	def selectedMover( self ) -> Mover:
		return self.__selectedMover

	@property
	def point( self ):
		return self.__point

	def setSelectionMode( self, mode ):
		self.__selectionMode = mode

	def __getNewEntry( self ):
		if self.__mouseWatcherNode.hasMouse():
			mousePosition = self.__mouseWatcherNode.getMouse()
			self.__generalPicker.pickerRay.setFromLens( self.__camNode, mousePosition.getX(), mousePosition.getY() )
			self.__generalPicker.picker.traverse( self.__render )
			numEntries = self.__generalPicker.pickerQueue.getNumEntries()
			if numEntries > 0:
				self.__generalPicker.pickerQueue.sortEntries()
				entry = self.__generalPicker.pickerQueue.getEntry( 0 )
				return entry

	def on_map_click( self ):
		entry = self.__getNewEntry()
		self.__point = entry.getSurfacePoint( self.__render )
		print( f'point: { self.__point }')
		self.__terrainCamera.setCenter( self.__point )
		picked_obj = entry.getIntoNodePath()
		if picked_obj is None:
			return
		print( f"Clicked node: { picked_obj }" )
		picked_item = picked_obj.node().getPythonTag( 'collision_target' )
		print( f"Clicked entity: { picked_item }" )
		if self.__selectionQueue.empty() and picked_item.isTerrain:
			self.__selectionMode = SelectionModes.CREATE
			self.__clearSelections( self.__clearSelection)
		elif picked_item.isMover:
			if self.__selectionQueue.empty():
				self.__clearSelections( self.__clearSelection )
			self.__selectionMode = SelectionModes.P2P

		self.__selectionQueue.put( picked_item )
		self.__selectionHandlers[ self.__selectionMode ].__call__()

	def __createSelection( self ):
		pick = self.__selectionQueue.get()
		pick.handleSelection( self.__selectionMode )
		self.__clearSelection.put( pick )

	def __p2pSelection( self ):
		tempQueue = queue.Queue()
		mover = self.__selectionQueue.get()
		if not mover.isMover:
			return
		mover.handleSelection( self.__selectionMode )
		self.__selectedMover = mover
		tempQueue.put( mover )
		while not self.__selectionQueue.empty():
			terrain = self.__selectionQueue.get()
			if terrain.isTerrain:
				terrain.handleSelection( self.__selectionMode )
				tempQueue.put( terrain )
			else:
				self.__clearSelections( tempQueue )
				return
		self.__selectionQueue = tempQueue

	def __clearSelections( self, selectionQueue ):
		while not selectionQueue.empty():
			selection = selectionQueue.get()
			selection.clearSelection()
		selectionQueue.empty()
