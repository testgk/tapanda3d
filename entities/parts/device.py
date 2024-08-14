from entities.parts.part import Part
from entities.parts.partsdb import parts


class Device( Part ):
    def __init__( self, partId ):
        super().__init__( parts.DEVICES, partId )