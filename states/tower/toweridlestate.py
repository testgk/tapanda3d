from states import IdleState


from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from entities.full.towers.towers import Tower

class TowerIdleState( IdleState ):
    def __init__( self, entity: 'Tower' ) -> None:
        super().__init__( entity )
        self._nextState = "idle"

    def execute( self ):
        return
