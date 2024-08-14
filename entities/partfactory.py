from typing import TYPE_CHECKING
from entities.parts.partutils import find_entity_parts

if TYPE_CHECKING:
    from entity import Entity

class PartFactory:
    def __init__(self, entity: 'Entity' ):
        self.__modules = None
        self.__parts = None
        self.__entity = entity

    def addParts( self ):
        self.__parts, self.__modules = find_entity_parts( self.__entity )

    def buildParts( self ):
        pass

    def renderAllParts( self ) :
        pass
