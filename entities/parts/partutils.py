from entities.parts.part import Part
from entities.modules.module import Module


def find_entity_parts( cls ) -> tuple[ list[ 'Part' ], list[ 'Module' ] ]:
    entityParts = []
    entityModules = []
    for name in dir( cls ):
        attr = getattr( cls, name)
        if getattr( attr, '_is_entitypart', False ):
            entityParts.append( name )
        elif getattr( attr, '_is_entitymodule', False ):
            entityModules.append( name )
    return entityParts, entityModules