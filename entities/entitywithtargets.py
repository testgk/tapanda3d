from collections import deque


class EntityWithTargets:
    def __init__( self ):
        self.__nextTarget = None
        self.__currentTarget = None
        self._selectedTargets: deque = deque()

    def clearCurrentTarget( self ):
        if not self.__currentTarget:
            return
        if self.__currentTarget is self.__nextTarget:
            self.__nextTarget = None
        self.__currentTarget = None

    def selectedTarget( self, target ) -> bool:
        return target is self.__nextTarget or target in self._selectedTargets
