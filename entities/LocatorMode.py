import random
from enum import Enum


class LocatorMode( Enum ):
	Right = 0
	Left = 1
	Target = 2
	Radius = 3
	All = ( Right, Left, Target )
	Edges = ( Left, Right )
	TargetOnly = ( Target )
