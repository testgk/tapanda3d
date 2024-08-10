from entities.entity import Entity
from statemachine.state import State


class ProcessCommandState( State ):
    def __init__( self, entity: Entity ):
        super().__init__( entity )

    def execute( self ):
        command = self._entity.pendingCommand()
