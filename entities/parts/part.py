from panda3d.core import BitMask32, LVector3

from enums.colors import Color


class Part:
    def __init__( self, partData = None, partId: str = None, external: bool = False, isRendered: bool = True, device = None, **kwargs ) :
        self._objectPath = ''
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
        self.__model = None
        self.__rigidBody = None
        self.__rigidBodyPath = None

    @property
    def objectPath( self ) -> str:
        return self._objectPath

    @property
    def rigidBodyPath( self ):
        return self.__rigidBodyPath

    @rigidBodyPath.setter
    def rigidBodyPath( self, path ) -> None:
        self.__rigidBodyPath = path

    @property
    def rigidBody( self ):
        return self.__rigidBody

    @rigidBody.setter
    def rigidBody( self, path ) -> None:
        self.__rigidBody = path

    @property
    def isRendered( self ) -> bool:
        return self.__isRendered

    @property
    def rigidGroup( self ) -> str:
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

    @property
    def model( self ):
        return self.__model

    @property
    def rigidBody( self ):
        return self.__rigidBody

    def setModel( self, model ):
        self.__model = model

    def setRigidBodyProperties( self, rigidBody ):
        self.__rigidBody = rigidBody
        if self.__friction is not None:
            self.__rigidBody.setAnisotropicFriction( self.__friction )
        self.__rigidBody.setIntoCollideMask( BitMask32.allOff() )
        self.__rigidBody.setIntoCollideMask( self.collideGroup )
        self.__rigidBody.setMass( self.__rigidBody.mass + self.mass )

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
