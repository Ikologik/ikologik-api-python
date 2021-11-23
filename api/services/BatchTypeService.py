from api.domain.Search import Search
from api.services.AbstractIkologikInstallationService import AbstractIkologikInstallationService


class BatchTypeService(AbstractIkologikInstallationService):

	# CRUD Actions

	def get_url(self, customer, installation):
		return f'{self.api_helper.get_url()}/api/v2/customer/{customer}/installation/{installation}/batchtype'

	def get_by_name(self, customer: str, installation: str, name):
		search = Search()
		search.add_filter = ("name", "EQ", [name])
		search.add_order("name", "ASC")

		# Query
		result = self.search(customer, installation, search)
		return result[0]
