from JwtHelper import JwtHelper
from api.domain.Search import Search
from api.services.AbstractIkologikInstallationService import AbstractIkologikInstallationService


class BatchService(AbstractIkologikInstallationService):

    def __init__(self, jwtHelper: JwtHelper):
        super().__init__(jwtHelper)

    # CRUD Actions

    def get_url(self, customer, installation):
        return f'{self.jwtHelper.get_url()}/api/v2/customer/{customer}/installation/{installation}/batch'

    def get_by_code(self, customer: str, installation: str, batchType: str, code: str):
        search = Search()
        # search.add_filter("batchType", "EQ", [batchType])
        search.add_multiple_filters([("batchType", "EQ", [batchType]), ("code", "EQ", [code])])
        search.add_order("batchType", "ASC")

        # Query
        result = self.search(customer, installation, search)
        if result:
            return result[0]
        else:
            return []
