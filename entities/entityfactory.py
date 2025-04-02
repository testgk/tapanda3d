from entities.full.movers.tank import Tank
from entities.full.towers.towers import TowerSmall
from entities.parts.engine import BasicEngine
from entities.modules.turret import CannonTurret
from entities.modules.mobilechassis import BasicTracksChassis
from entities.parts.obstacles.cube import Cube, BigCube


class EntityFactory:
    @staticmethod
    def create_entity( entityType: str ):
        creator = EntityRegistry.getCreator( entityType )
        if creator:
            return creator()
        raise ValueError( f"Unknown entity type: { entityType }" )


class EntityRegistry:
    __entityCreators = {
        "basic_tank": lambda: Tank(
            engine = BasicEngine(),
            turret = CannonTurret(),
            axis = BasicTracksChassis()
        ),
        "cube": lambda: BigCube(),
        "tower_small": lambda: TowerSmall(),
    }

    @staticmethod
    def getCreator( entity_type ):
        return EntityRegistry.__entityCreators.get( entity_type )
