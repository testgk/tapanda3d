from statemachine.state import State


class Command:
    def __init__( self, name ):
        self.__name = None
        self.__progress = None
        self.__matchingState = None
        self.__isSerial = False

    @property
    def isSerial( self ) -> bool:
        return self.__isSerial

    @property
    def progress( self ) -> int:
        return self.__progress

    @property
    def matchingState( self ) -> State:
        return self.__matchingState