from panda3d.core import *
from panda3d.physics import *

# Set up the physics manager
physics_mgr = PhysicsManager()

# Set up the global physics clock
globalClock = ClockObject.getGlobalClock()
globalClock.setMode(ClockObject.MNonRealTime)
globalClock.setDt(1.0 / 60.0)


def generatePhysicsNode( render ):
    # Create a physics node
    physics_node = PhysicalNode( 'physics_node' )
    physics_np = render.attachNewNode( physics_node )

    # Attach the node to the physics manager
    physics_mgr.attachPhysicalNode( physics_node )
    # Create a linear force (e.g., gravity)
    gravity = LinearVectorForce( 0, 0, -9.81 )  # Gravity pulling downwards
    gravity_node = ForceNode( 'world-forces' )
    gravity_node.addForce( gravity )

    # Attach the force node to the scene graph
    gravity_np = render.attachNewNode( gravity_node )

    # Attach the force to the physics manager
    physics_mgr.addLinearForce( gravity )



