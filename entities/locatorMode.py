import random
from enum import Enum

from enums.colors import Color


class Locators( Enum ):
	Right = 0
	Left = 1
	Target = 2
	Dynamic = 3

class LocatorModes( Enum ):
	All = ( Locators.Right, Locators.Left, Locators.Target )
	Edges = ( Locators.Left, Locators.Right )
	TargetOnly = ( Locators.Target, Locators.Target )
	DynamicOnly = ( Locators.Dynamic, Locators.Dynamic )

locatorColors = {
		Locators.Right.value: Color.BLUE,
		Locators.Left.value: Color.BLUE,
		Locators.Target.value: Color.YELLOW,
		Locators.Dynamic.value: Color.ORANGE,
	}

