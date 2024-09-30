from camera import TerrainCamera
from entities.entity import Entity
from selector.selector import Selector


class Selectionmanager:
    def __init__( self, selector: Selector ):
        self.__selector = selector

    def handleSelection( self, selectedItem ):
        pass

    @property
    def selectedEntity( self ):
        return self.__selectedEntity
        
        