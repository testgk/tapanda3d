class PartBuilder:
    def addPart( self, part ):
        pass

    def addParts( self, _parts ):
        pass

    def renderAllParts( self ):
        pass


class Entity:
    def __init__( self ):
        self.name = None
        self._id = None
        self._stationary = None
        self._producer = None
        self._parts = None
        self._partBuilder = PartBuilder()

    def build( self ):
        self._setParts()
        self._createParts()

    def _setParts( self ):
        raise NotImplementedError

    def _createParts( self ):
        self._partBuilder.addParts( self._parts )
        self._partBuilder.renderAllParts()
