from entities.parts.partsdb import getPartsData


class Part:
	def __init__(self, partData, partId, ** kwargs ):
		part_data = partData.get( partId )
		if not part_data:
			raise ValueError( f"No data found for - { partId } in JSON file." )
		self.__metal = part_data[ "metal" ]
		self.__energy = part_data[ "energy" ]
		self.__protection = part_data[ "protection" ]
		self.__damage = part_data[ "damage" ]
		self._renderId = None
