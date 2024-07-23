from entities.entity import Entity


class Mover( Entity ):
    def __init__(self):
        super().__init__()
        self._currentPosition = None
        self._topSpeed = 0
        self._bottomSpeed = 0
        pass

    def move(self, destination):
        pass

    def stop(self):
        pass

    def turn( self, degrees ):
        pass

