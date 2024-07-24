import os.path

from entities.entity import Entity
from objects.stltoeggconverter import convert_stl_to_egg


class EntityLoader:
    def __init__( self, loader, entity: Entity ):
        self.__loader = loader
        self.__entity = entity
        self.__partEggFiles = {}
        self.__generateParts()

    def __generateParts( self  ):
        basePath = f"objects/{ self.__entity.name}/"
        for part in self.__entity.parts:
            stlPath = os.path.join( basePath, part, ".stl" )
            eggPath = stlPath.replace( ".stl", ".egg" )
            convert_stl_to_egg( stlPath, eggPath )
            self.__partEggFiles[ part ] = { "path": eggPath }

    def loadParts( self ):
        for part in self.__entity.parts:
            model = self.__loader.loadModel( self.__partEggFiles[ part ] )
            self.__partEggFiles[ part ][ "model" ] = model
