import json
from types import SimpleNamespace

import requests

from ikologikapi.IkologikApiCredentials import IkologikApiCredentials
from ikologikapi.IkologikException import IkologikException


class GraphService:
    def __init__(self, jwtHelper: IkologikApiCredentials):
        self.jwtHelper = jwtHelper

    # CRUD actions

    def get_headers(self, headers=None):
        default_headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.jwtHelper.get_jwt()}'
        }
        if headers is not None:
            default_headers.update(headers)
        return default_headers

    def get_url(self, customer: str, installation: str) -> str:
        return f'{self.jwtHelper.get_url()}/api/v2/customer/{customer}/installation/{installation}/graphmeter'

    def get_url_graph(self, customer: str, installation: str, id: str) -> str:
        return f'{self.jwtHelper.get_url()}/api/v2/customer/{customer}/installation/{installation}/graphmeter/{id}/graph'

    def get_graph_meter_list(self, customer, installation):
        try:
            response = requests.get(
                self.get_url(customer, installation),
                headers=self.get_headers()
            )
            if response.status_code == 200:
                result = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
                return result
            else:
                raise IkologikException(
                    "Error while performing get_graph_meter_list, the request returned status " + str(
                        response.status_code))
        except IkologikException as ex:
            raise ex
        except Exception as ex:
            raise IkologikException("Error while performing get_graph_meter_list")

    def search_graph_meter_list(self, customer, installation, search):
        try:
            data = json.dumps(search, default=lambda o: o.__dict__)
            response = requests.post(
                f'{self.get_url(customer, installation)}/search',
                data=data,
                headers=self.get_headers()
            )
            if response.status_code == 200:
                result = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
                return result
            else:
                raise IkologikException(
                    "Error while performing search, the request returned status " + str(response.status_code))
        except IkologikException as ex:
            raise ex
        except Exception as ex:
            raise IkologikException("Error while performing search")

    def get_active_meter_list(self, customer, installation):
        try:
            response = requests.get(
                f'{self.get_url(customer, installation)}/active',
                headers=self.get_headers()
            )
            if response.status_code == 200:
                result = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
                return result
            else:
                raise IkologikException(
                    "Error while performing get_active_meter_list, the request returned status " + str(
                        response.status_code))
        except IkologikException as ex:
            raise ex
        except Exception as ex:
            raise IkologikException("Error while performing get_active_meter_list")

    def search_active_meter_list(self, customer, installation, search):
        try:
            data = json.dumps(search, default=lambda o: o.__dict__)
            response = requests.post(
                f'{self.get_url(customer, installation)}/active/search',
                data=data,
                headers=self.get_headers()
            )
            if response.status_code == 200:
                result = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
                return result
            else:
                raise IkologikException(
                    "Error while performing search, the request returned status " + str(response.status_code))
        except IkologikException as ex:
            raise ex
        except Exception as ex:
            raise IkologikException("Error while performing search")

    def get_graph_meter(self, customer, installation, meter_id):
        try:
            response = requests.get(
                f'{self.get_url(customer, installation)}/{meter_id}',
                headers=self.get_headers()
            )
            if response.status_code == 200:
                result = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
                return result
            else:
                raise IkologikException(
                    "Error while performing get_active_meter_list, the request returned status " + str(
                        response.status_code))
        except IkologikException as ex:
            raise ex
        except Exception as ex:
            raise IkologikException("Error while performing get_active_meter_list")

    def get_data(self, customer, installation, meter_id, start_date, end_date):
        try:
            return self.get_data_with_data_type(customer, installation, meter_id, 'DATA', start_date, end_date)
        except IkologikException as ex:
            raise ex
        except Exception as ex:
            raise IkologikException("Error while performing get_data")

    def get_data_with_data_type(self, customer, installation, meter_id, data_type, start_date, end_date):
        try:
            response = requests.get(
                f'{self.get_url_graph(customer, installation, meter_id)}/{data_type}/{start_date}/{end_date}',
                headers=self.get_headers()
            )
            if response.status_code == 200:
                result = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
                return result
            else:
                raise IkologikException(
                    "Error while performing get_active_meter_list, the request returned status " + str(
                        response.status_code))
        except IkologikException as ex:
            raise ex
        except Exception as ex:
            raise IkologikException("Error while performing get_active_meter_list")

    def get_graph_data(self, customer, installation, meter_id, data_type, start_date, end_date, limit, auto_reduce):
        try:
            response = requests.get(
                self.get_url_graph(customer, installation, meter_id) + f'/data/{data_type}/{start_date}/{end_date}',
                params={'limit': limit, 'autoReduce': auto_reduce},
                headers=self.get_headers()
            )
            if response.status_code == 200:
                result = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
                return result
            else:
                raise IkologikException(
                    "Error while performing get_data, the request returned status " + str(response.status_code))
        except IkologikException as ex:
            raise ex
        except Exception as ex:
            raise IkologikException("Error while performing get_by_id")

    def get_graph_alerts(self, customer, installation, meter_id, start_date, end_date):
        try:
            response = requests.get(
                self.get_url_graph(customer, installation, meter_id) + f'/alerts/{start_date}/{end_date}',
                headers=self.get_headers()
            )
            if response.status_code == 200:
                result = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
                return result
            else:
                raise IkologikException(
                    "Error while performing get_data, the request returned status " + str(response.status_code))
        except IkologikException as ex:
            raise ex
        except Exception as ex:
            raise IkologikException("Error while performing get_by_id")

    def get_graph_navigator_data_list(self, customer, installation, meter_id):
        try:
            response = requests.get(
                self.get_url(customer, installation) + f'/{meter_id}/navigatordata',
                headers=self.get_headers()
            )
            if response.status_code == 200:
                result = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
                return result
            else:
                raise IkologikException(
                    "Error while performing get_data, the request returned status " + str(response.status_code))
        except IkologikException as ex:
            raise ex
        except Exception as ex:
            raise IkologikException("Error while performing get_by_id")
