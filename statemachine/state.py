from entities.entity import Entity
from statemachine.event import Event


class State:
    def __init__( self, entity: Entity ):
        self.__entity = entity
        self.__enterEvent = Event()
        self.__exitEvent = Event()

    def enter( self ):
        self.__enterEvent.notify()

    def exit( self ):
        self.__exitEvent.notify()

    def execute( self ):
        pass

    def _reportState( self, stage: str ):
        print( f'{ self.__entity } { stage } state: { self }' )


    @staticmethod
    def create_state_instance( class_name, *args ) :
        # Look up the class by name in the global namespace
        cls = globals().get( class_name )
        if cls is not None :
            return cls( *args )
        else :
            raise ValueError( f"Class '{class_name}' not found." )

