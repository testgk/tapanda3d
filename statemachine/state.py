from entities.entity import Entity
from statemachine.eventmetaclass import EventMetaclass


class State( metaclass = EventMetaclass ):
    def __init__( self, entity: Entity ):
        self.possibleNextStates = None
        self._nextState = None
        self._entity = entity
        self._setStatesPool()

    def enter( self ):
        pass

    def exit( self ):
        pass

    def execute( self ):
        pass

    def _setStatesPool( self ):
        pass

    def decideNextState( self ) -> 'State':
        return self._entity.decide()
