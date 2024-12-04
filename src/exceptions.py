class ShopifyClientError(Exception):
    pass

class ShopifyBadTokenException(ShopifyClientError):
    pass

class ShopifyForbidden(ShopifyClientError):
    pass

class ShopifyPaymentRequiredError(ShopifyClientError):
    pass

class ShopifyResourceNotFoundError(ShopifyClientError):
    pass

class ShopifyShopLockedError(ShopifyClientError):
    pass


class ValidationError(ValueError):
    pass

class InvlidArgument(ValueError):
    pass

class NotEnoughtArguments(ValueError):
    pass
