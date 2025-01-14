from selectionitem import SelectionItem


class Target( SelectionItem ):
	def __init__( self ):
		super().__init__()

	@property
	def position( self ):
		return NotImplemented
