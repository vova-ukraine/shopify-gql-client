from client import ShopifyGraphQLClient

from schema.queries.shop import ShopQuery, QueryRootQuery
from schema.queries.catalogs import Catalogs
from schema.objects.query_root import QueryRoot
from schema.objects.shop import Shop
from schema.objects.shop_address import ShopAddress
from schema.objects.company import Company
from schema.objects.app_installation import AppInstallation
from schema.objects.app_subscription import AppSubscription
from schema.objects.app_plan_v2 import AppPlanV2
from schema.objects.app_subscription_line_item import AppSubscriptionLineItem
from schema.objects.app_recurring_pricing import AppRecurringPricing
from schema.objects.money_v2 import MoneyV2
from schema.objects.app_usage_pricing import AppUsagePricing
from schema.interfaces.catalog import Catalog
# from schema.objects.currency_formats import CurrencyFormats

from schema.queries.app_installation import AppInstallationQuery
from schema.objects.catalog_connection import CatalogConnection

from on import on



import logging

logging.basicConfig(level=logging.DEBUG)

shop_name = "embedded-adwisely.myshopify.com" 
access_token = ""

client = ShopifyGraphQLClient(shop_name, access_token)

# query = ShopQuery(
#     fields=[
#         Shop.Fields.id,
#         Shop.Fields.name,
#         Shop.Fields.myshopify_domain,
#         Shop.Fields.billing_address[
#             ShopAddress.Fields.address1,
#             ShopAddress.Fields.city,
#             ShopAddress.Fields.address2
#         ],
#         # Shop.Fields.currency_code,
#         # Shop.Fields.currency_formats[
#         #     CurrencyFormats.Fields.money_format,
#         #     CurrencyFormats.Fields.money_with_currency_format
#         # ]
#     ]
# )

# def get_shop() -> Shop:
#     response = client.send_queries([query])
#     return response[0]

# shop = get_shop()
# print(shop.__dict__)

# query = QueryRootQuery(
#     fields=[
#         QueryRoot.Fields.company(id="23")[
#             Company.Fields.id,
#         ]
#     ]
# )

# print(query)


# query = AppInstallationQuery(fields=[
#                 AppInstallation.Fields.active_subscriptions[
#                 AppSubscription.Fields.line_items[
#                     AppSubscriptionLineItem.Fields.plan[
#                         AppPlanV2.Fields.pricing_details[
#                             on(AppRecurringPricing, [
#                                 AppRecurringPricing.Fields.price[
#                                     MoneyV2.Fields.amount,
#                                     MoneyV2.Fields.currency_code
#                                 ]
#                             ]),
#                             on(AppUsagePricing, [
#                                 AppUsagePricing.Fields.capped_amount[
#                                     MoneyV2.Fields.amount,
#                                     MoneyV2.Fields.currency_code
#                                 ]
#                             ])
#                         ],
#                     ],
#                 ],
#             ],
#         ]
#     )

# def get_app_installation() -> AppInstallation:
#     response = client.send_queries([query])
#     return response[0]

# app_installation = get_app_installation()
# print(app_installation.active_subscriptions[0].line_items[0].plan.pricing_details.capped_amount.amount)


query = Catalogs(first=1)[
        CatalogConnection.Fields.nodes[
            "id",
            "title",
        ],
    ]

response = query.query(client)
print(response.nodes[0].__dict__)

# def get_catalogs() -> CatalogConnection:
#     response = client.send_queries([query])
#     return response[0]

# catalogs = get_catalogs()
# print(catalogs.__dict__)