from entities.mover import Mover


class Tank( Mover ):
    def __init__( self ):
        super().__init__()
        self.parts = [ 'body', 'turret' ]
