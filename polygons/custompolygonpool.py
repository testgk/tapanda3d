from typing import TYPE_CHECKING

from enums.directions import mapDirections

if TYPE_CHECKING:
    from customcollisionpolygon import CustomCollisionPolygon

class CustomPolygonPool:
    _instance = None
    _polygons = {}

    def __new__( cls, *args, **kwargs ):
        if not cls._instance:
            cls._instance = super( CustomPolygonPool, cls ).__new__( cls, *args, **kwargs )
        return cls._instance

    @classmethod
    def Instance( cls ) -> 'CustomPolygonPool':
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def getPolygonFromPool( self, row: int, column: int ) -> 'CustomCollisionPolygon':
        try:
            return CustomPolygonPool._polygons[ f"gmm{ row }x{ column }" ]
        except KeyError:
            return None

    def getPolygonByName( self, name: str) -> 'CustomCollisionPolygon':
        return CustomPolygonPool._polygons[ name ]

    def addPolygonToPool( self, name: str, polygon: 'CustomCollisionPolygon' ):
        CustomPolygonPool._polygons[ name ] = polygon

    def acquireAllNeighbors( self ):
        for name, polygon in self._polygons.items():
            self.__getNeighbors( polygon )

    def __getNeighbors( self, polygon: 'CustomCollisionPolygon' ):
        neighborsDic = { }
        for direction, val in mapDirections.items():
            neighborsDic[ direction ] = self.getPolygonFromPool( polygon.row + val[ 0 ], polygon.col + val[ 1 ] )
        polygon.neighbors = { pos: node for pos, node in neighborsDic.items() if node is not None }
