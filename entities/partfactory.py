import os

from typing import TYPE_CHECKING ,Callable

from panda3d.core import NodePath

if TYPE_CHECKING:
    from entities.entity import Entity
    from entities.parts.part import Part

from objects.stltoeggconverter import convert_stl_to_egg


def find_entity_parts( cls ) -> tuple[ list[ Callable ], list[ Callable ] ]:
    entityParts = []
    entityModules = []
    for name in dir( cls ):
        attr = getattr( cls, name)
        if getattr( attr, '_is_entitypart', False ):
            entityParts.append( attr )
        elif getattr( attr, '_is_entitymodule', False ):
            entityModules.append( attr )
    return entityParts, entityModules


class PartFactory:
    def __init__(self, entity: 'Entity' ):
        self.__modules = []
        self.__parts = []
        self.__entity = entity

    def addParts( self ):
        parts, modules = find_entity_parts( self.__entity )
        for part in parts:
            self.__parts.append( part() )
        for module in modules:
            self.__modules.append( module() )

    def modules( self ):
        return self.__modules

    def parts( self ):
        return self.__parts

    def buildAllParts( self, loader ) -> list[ NodePath ]:
        models = []
        for part in self.__parts:
            if not part.isRendered:
                continue
            try :
                eggPath = self.__getPartEggPath( part )
                models.append(  loader.loadModel( eggPath ) )
            except:
                pass
        return models

    def __getPartEggPath( self, part: 'Part' ):
        fullPath = os.path.join( "objects/parts/" ,part.objectPath, part.partId )
        eggPath = fullPath + ".egg"
        if os.path.exists( eggPath ):
            return eggPath
        else:
            stlPath = fullPath + ".stl"
            if os.path.exists( stlPath ):
                convert_stl_to_egg( stlPath ,eggPath )
                return eggPath
