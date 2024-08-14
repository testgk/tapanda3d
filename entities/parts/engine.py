from entities.parts.part import Part


class Engine( Part ):
    def __init__( self, ** kwargs ):
        super().__init__( ** kwargs )