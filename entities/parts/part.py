from panda3d.core import LVector3

from enums.colors import Color


class Part:
    def __init__( self, partData = None, partId: str = None, external: bool = False, isRendered: bool = True, device = None, **kwargs ) :
        self.__rigidGroup = None
        self.collideGroup = 0
        self.__device = device
        self._external = external
        self.__partId = partId
        self.__isRendered = isRendered
        self._color = Color.WHITE.value
        self.__friction = LVector3( 0.01, 10, 0.0 )
        self._mass = 50
        if partId and partData:
            part_data = partData.get( partId )
            self._readPartData( part_data )

    @property
    def objectPath( self ) -> str:
        return ''

    @property
    def isRendered( self ) -> bool:
        return self.__isRendered

    @property
    def rigidGroup( self ):
        return self.__rigidGroup

    @property
    def color( self ):
        return self._color

    @property
    def mass( self ):
        return self._mass

    @property
    def partId( self ) -> str:
        return self.__partId

    def _readPartData( self, part_data ) :
        self.__metal = part_data[ "metal" ]
        self.__energy = part_data[ "energy" ]
        self._mass = part_data.get( "mass", self._mass )
        if self._external:
            self.__protection = part_data[ "protection" ]
            self.__damage = part_data[ "damage" ]

    def setRigidGroup( self, group: str ):
        self.__rigidGroup = group

    def setCollideGroup( self, collideGroup ):
        self.collideGroup = collideGroup
