class NotFoundError(Exception):
	def __init__(self, entity: str, identifier: str):
		self.entity = entity
		self.identifier = identifier
		super().__init__(f"{entity} with {identifier} does not exist.")


class DuplicateError(Exception):
	def __init__(self, entity: str, detail: str = ""):
		self.entity = entity
		self.detail = detail
		msg = f"{entity} already exists."
		if detail:
			msg += f" {detail}"
		super().__init__(msg)


class InvalidGeometryError(Exception):
	def __init__(self, detail: str = "Incorrect input field geom."):
		super().__init__(detail)
