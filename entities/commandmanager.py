from statemachine.commands.command import Command


class CommandManager:
    def __init__( self ):
        self._commands = None
        self.__pendingCommand = None

    def receiveCommand( self, command: Command ):
        self._commands.insert( 0, command )

    def pendingCommand( self ) -> Command | None:
        if self.__pendingCommand is None:
            self.__pendingCommand = self._commands.pop()
        if self.__pendingCommand.progress == 0:
            return self.__pendingCommand
