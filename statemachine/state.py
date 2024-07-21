from entities.entity import Entity


class State:
    def __init__( self, entity: Entity ):
        self.__entity = entity

    def enter( self ):
        pass

    def exit( self ):
        pass

    def execute( self ):
        pass