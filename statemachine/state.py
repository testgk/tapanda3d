from statemachine.eventmetaclass import EventMetaclass


class State( metaclass = EventMetaclass ):
    def __init__( self, entity):
        self._nextState = None
        self._entity = entity
        self._done = False

    @property
    def done( self ) -> bool:
        return self._done

    @property
    def nextState( self ) -> 'str':
        return self._nextState

    @nextState.setter
    def nextState( self, state ) -> None:
        self._nextState = state

    def initialize( self ):
        self._done = False
        self._nextState = None

    def doneState( self, nextState: str ) -> None:
        self._done = True
        self._nextState = nextState

    def enter( self ):
        raise NotImplementedError

    def exit( self ):
        print( f'{ self._entity.name } Exited { self.__class__.__name__ } state' )

    def execute( self ):
        raise NotImplementedError

    def __str__( self ):
        return self.__class__.__name__

    def __eq__( self, other: str ):
        return self.__class__.__name__ == other
