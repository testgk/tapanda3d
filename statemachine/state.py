from statemachine.eventmetaclass import EventMetaclass


class State( metaclass = EventMetaclass ):
    def __init__( self, entity ):
        self.possibleNextStates = None
        self._nextState = None
        self._entity = entity
        self._setStatesPool()
        self._done = False

    @property
    def done( self ) -> bool:
        return self._done

    @property
    def nextState( self ) -> 'State':
        return self._nextState

    @nextState.setter
    def nextState( self, state ) -> None:
        self._nextState = state

    def enter( self ):
        print( f'{ self._entity.name } Entered { self.__class__.__name__ } state' )

    def exit( self ):
        print( f'{ self._entity.name } Exited { self.__class__.__name__ } state' )

    def execute( self ):
        raise NotImplementedError

    def _setStatesPool( self ):
        pass

    def decideNextState( self ) -> 'State':
        self._nextState = self._entity.decide()
        return self._nextState

    def __str__( self ):
        return self.__class__.__name__
