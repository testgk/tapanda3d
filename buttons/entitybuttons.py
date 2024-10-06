from direct.gui.DirectButton import DirectButton

from entities.entityphysics import Entityphysics
from selector.selector import Selector


class EntityButtons:
    def __init__( self, selector: Selector ):
        self.__selector = selector
        self.create_allign_button()

    def create_allign_button( self ):
        alignButton = DirectButton(
            text = "Allign",
            command = self.__applyVelocity,
            pos = ( 0, -0.7, -0.7),
            text_scale = 0.5,
            scale = 0.1
        )

    def __applyVelocity( self ):
        Entityphysics.applyVelocity( self.__selector.selectedEntity )