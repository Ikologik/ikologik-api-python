from api.domain.AbstractIkologikObject import AbstractIkologikObject


class AbstractIkologikCustomerObject(AbstractIkologikObject):
	customer: str = None

	def __init__(self, customer: str):
		super().__init__()
		self.customer = customer
