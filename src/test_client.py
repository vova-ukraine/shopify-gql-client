from config import Config
from client import ShopifyGraphQLClient

from schema.objects.shop import Shop
from schema.objects.app_installation import AppInstallation
from schema.objects.app_subscription import AppSubscription
from schema.objects.app_plan_v2 import AppPlanV2
from schema.objects.app_subscription_line_item import AppSubscriptionLineItem
from schema.objects.app_recurring_pricing import AppRecurringPricing
from schema.objects.money_v2 import MoneyV2
from schema.objects.app_usage_pricing import AppUsagePricing
from schema.objects.product import Product
from schema.objects.product_connection import ProductConnection
from local_credentials import SHOP_NAME, ACCESS_TOKEN

from on import on

import logging

logging.basicConfig(level=logging.DEBUG)


client = ShopifyGraphQLClient(SHOP_NAME, ACCESS_TOKEN)

shop = client.query_shop(
    fields=[
        Shop.Fields.id,
        Shop.Fields.name,
        Shop.Fields.myshopify_domain,
    ]
)


print(shop.name)

products = client.query_products(
    args={
        "first": 10
    },
    fields=[
        ProductConnection.Fields.nodes[
            Product.Fields.id,
            Product.Fields.title,
        ],
    ]
)

for product in products.nodes:
    print(product.body_html)

Config.unpopulated_fields_warning = False

for product in products.nodes:
    try:
        print(product.body_html)
    except AttributeError as e:
        print(e)


app_installation = client.query_app_installation(fields=[
                AppInstallation.Fields.active_subscriptions[
                AppSubscription.Fields.line_items[
                    AppSubscriptionLineItem.Fields.plan[
                        AppPlanV2.Fields.pricing_details[
                            on(AppRecurringPricing, [
                                AppRecurringPricing.Fields.price[
                                    MoneyV2.Fields.amount,
                                    MoneyV2.Fields.currency_code
                                ]
                            ]),
                            on(AppUsagePricing, [
                                AppUsagePricing.Fields.capped_amount[
                                    MoneyV2.Fields.amount,
                                    MoneyV2.Fields.currency_code
                                ]
                            ])
                        ],
                    ],
                ],
            ]
        ]
    )

print(len(app_installation.active_subscriptions))