from panda3d.core import CollisionHandlerPusher


class MyCollisionHandlerPusher( CollisionHandlerPusher ):
    def __init__(self):
        CollisionHandlerPusher.__init__(self)

    def handleEntries(self):
        for entry in self.entries:
            print(f"Collision detected:")
            print(f"  From: { entry.getFromNodePath().getName()}")
            print(f"  Into: { entry.getIntoNodePath().getName()}")
            print(f"  At: { entry.getSurfacePoint(entry.getIntoNodePath())}")