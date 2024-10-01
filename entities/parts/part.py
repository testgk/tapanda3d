from entities.entity import PartFactory


class Part:
    def __init__( self, partData, partId, external: bool = False, **kwargs ) :
        self._external = external
        self.__partFactory = None
        part_data = partData.get( partId )
        self._readPartData( part_data )
        if self.hasParts :
            self.__partFactory = PartFactory( self )

    @property
    def hasParts( self ) -> bool :
        return False

    @property
    def partFactory( self ):
        return self.__partFactory

    def _readPartData( self, part_data ) :
        self.__metal = part_data[ "metal" ]
        self.__energy = part_data[ "energy" ]
        if self._external:
            self.__protection = part_data[ "protection" ]
            self.__damage = part_data[ "damage" ]
            self._renderId = None
