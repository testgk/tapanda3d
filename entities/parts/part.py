import os.path


class Part:
    def __init__( self, partData, partId: str = None, external: bool = False, isRendered: bool = True, device = None, **kwargs ) :
        self.__device = device
        self._external = external
        self.__partId = partId
        self.__isRendered = isRendered
        if partId is not None:
            part_data = partData.get( partId )
            self._readPartData( part_data )

    @property
    def objectPath( self ) -> str:
        return ''

    @property
    def isRendered( self ) -> bool:
        return self.__isRendered

    @property
    def partId( self ) -> str:
        return self.__partId

    def _readPartData( self, part_data ) :
        self.__metal = part_data[ "metal" ]
        self.__energy = part_data[ "energy" ]
        if self._external:
            self.__protection = part_data[ "protection" ]
            self.__damage = part_data[ "damage" ]
