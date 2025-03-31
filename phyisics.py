from panda3d.core import *
from panda3d.physics import *

# Set up the physics manager
physics_mgr = PhysicsManager()

# Set up the global physics clock
globalClock = ClockObject.getGlobalClock()
globalClock.setMode( ClockObject.MNonRealTime )
globalClock.setDt( 1.0 / 60.0 )




