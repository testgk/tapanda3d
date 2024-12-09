from typing import TYPE_CHECKING
from statemachine.state import State

if TYPE_CHECKING:
    from entities.full.movers.mover import Mover

class MovementState( State ):
    def __init__( self, entity: 'Mover' ):
        super().__init__( entity )

    @property
    def entity( self ) -> 'Mover':
        return self._entity

    def enter( self ):
        self.entity.schedulePointToPointTask()

    def execute( self ):
        if self.entity.finishedMovement():
            self._done = True
            print( f'{self._entity.name} finished moving' )
        else:
            print( f'{ self._entity.name } moving' )
