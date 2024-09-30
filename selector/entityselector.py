from camera import TerrainCamera
from entities.entity import Entity


class EntitySelector:
    def __init__( self ,terrain ,terrainPicker ,mouseWatcherNode ,camNode ,terrainCamera: TerrainCamera ,physicsWorld , render ):
        self.__selectedEntity = None

    def selectEntity( self, entity: Entity ):
        self.__selectedEntity = entity

    @property
    def selectedEntity( self ):
        return self.__selectedEntity
        
        