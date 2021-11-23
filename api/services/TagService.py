import json
from types import SimpleNamespace

import requests

from api.services.AbstractIkologikInstallationService import AbstractIkologikInstallationService


class TagService(AbstractIkologikInstallationService):

	def get_url(self, customer, installation):
		return f'{self.api_helper.get_url()}/api/v2/customer/{customer}/installation/{installation}/tag'

	def create(self, customer, installation, o: object) -> object:
		try:
			response = requests.post(
				self.get_url(customer, installation),
				data=json.dumps(o.__dict__),
				headers=self.get_headers()
			)
			result = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
			return result
		except requests.exceptions.HTTPError as error:
			print(error)
