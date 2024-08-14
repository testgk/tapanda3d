from statemachine.state import State


class ProcessCommandState( State ):
    def __init__( self, entity ):
        super().__init__( entity )
        self.__command = None

    def execute( self ):
        self.__command = self._entity.pendingCommand()

    def decideNextState( self ) -> 'State':
        return self.__command.matchingState
