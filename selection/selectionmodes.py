from enums.colors import Color


class SelectionModes:
	NONE = 0
	ANY = 1
	P2P = 2
	ATTACK = 3
	CREATE = 4
	CHECK = 5
	TARGET = 6
	ORIGINAL_TARGET = 8
	TEMP = 7

	selectioColors = {
		CREATE: Color.BLUE,
		CHECK: Color.RED,
		P2P: Color.YELLOW,
		TARGET: Color.ORANGE,
		ORIGINAL_TARGET: Color.CYAN,
		TEMP: Color.MAGENTA,
		ANY: Color.MAGENTA,
		ATTACK: Color.RED
	}

	@staticmethod
	def selectionColors( mode: int ):
		return SelectionModes.selectioColors[ mode ]
