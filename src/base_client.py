import logging
import json
from urllib import request, error

from classes import Queryable

from exceptions import (
    ShopifyBadTokenException,
    ShopifyForbidden,
    ShopifyPaymentRequiredError,
    ShopifyClientError,
    ShopifyResourceNotFoundError,
    ShopifyShopLockedError,
)

logger = logging.getLogger(__name__)

status_codes_errors = {
    401: ShopifyBadTokenException,
    402: ShopifyPaymentRequiredError,
    403: ShopifyForbidden,
    404: ShopifyResourceNotFoundError,
    423: ShopifyShopLockedError,
}


class BaseShopifyGraphQLClient:

    SHOPIFY_API_VERSION = "2024-10"

    def __init__(self, shop_name: str, access_token: str):
        self.url = f"https://{shop_name}/admin/api/{self.SHOPIFY_API_VERSION}/graphql.json"
        self.access_token = access_token

    def send_queries(self, queries: list[Queryable], variables=None):
        json_data = self.request(queries, variables)
        return self._parse_data(queries, json_data)

    def request(self, queries: list[Queryable], variables=None):
        headers = {
            "X-Shopify-Access-Token": self.access_token,
            "Content-Type": "application/json",
        } 

        query = "{" + "\n".join(map(lambda query: str(query), queries)) + "}"

        if variables:
            logger.debug(f"Shopify GraphQL variables: {variables}")

        try:
            data = json.dumps({"query": query, "variables": variables}).encode('utf-8')

            logger.debug(f"Shopify GraphQL data: {data}")

            req = request.Request(
                self.url,
                data=data,
                headers=headers,
                method='POST'
            )

            # TODO: add custom user agent
            with request.urlopen(req) as response:
                if response.status != 200:
                    self._raise_http_status_error(response)

                response_data = response.read()
                json_response = json.loads(response_data)

                logger.debug(f"Shopify GraphQL JSON response: {json_response}")

                if "errors" in json_response:
                    self._raise_graphql_errors(json_response)

                return json_response["data"]

        except error.HTTPError as e:
            self._raise_http_status_error(e)
        except json.JSONDecodeError as e:
            raise ShopifyClientError(
                "Shopify GraphQL request error. Response is not a valid JSON"
            )
        except error.URLError as e:
            raise ShopifyClientError("Shopify GraphQL request error")

    def _raise_http_status_error(self, response):
        error_message = ""
        try:
            error_data = response.read()
            error_message = json.loads(error_data)["errors"]
        except Exception:
            error_message = (
                "Shopify GraphQL request error with status code %s"
                % response.code
            )

        status_code = response.code
        if status_code in status_codes_errors:
            raise status_codes_errors[status_code](error_message)

        if status_code >= 500:
            raise ShopifyClientError("Shopify GraphQL Internal Server Error")

        raise ShopifyClientError(error_message)

    def _raise_graphql_errors(self, json_response):
        raise ShopifyClientError(json_response["errors"][0]["message"])
    
    def _parse_data(self, queries, data: dict):
        result = []
        for query in queries:
            result.append(query.root_field.get_type_class()(data[query.root_field.name]))
        return result
