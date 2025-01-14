import random
from enum import Enum

from enums.colors import Color


class Locators( Enum ):
	NONE = 0
	Right = 1
	Left = 2
	Target = 3
	Dynamic = 4
	TargetRight = 5
	TargetLeft = 6


class LocatorModes( Enum ):
	NONE = None
	All = ( Locators.Right, Locators.Left )
	Edges = ( Locators.Left, Locators.Right )
	TargetEdges = ( Locators.TargetLeft, Locators.TargetRight )
	TargetOnly = ( Locators.Target, Locators.Target )
	DynamicOnly = ( Locators.Dynamic, Locators.Dynamic )

locatorColors = {
		Locators.Right.value: Color.BLUE,
		Locators.Left.value: Color.BLUE,
		Locators.Target.value: Color.YELLOW,
		Locators.Dynamic.value: Color.ORANGE,
	}

