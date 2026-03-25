from __future__ import annotations

from framework.config.config_manager import ConfigManager
from services.product_catalog_service.product_catalog_service_api import ProductCatalogServiceAPI
from services.product_catalog_service.product_catalog_service_models import (
    GetProductByIdRequest,
    Product,
    ProductPrice,
)
from services.product_catalog_service.product_catalog_service_request import ProductCatalogServiceRequest


def get_product_by_id(config: ConfigManager, request: GetProductByIdRequest) -> Product:
    request_data = ProductCatalogServiceRequest.get_product_by_id_request(request)
    response = ProductCatalogServiceAPI(config).get_product_by_id(product_id=request_data["product_id"])
    assert response.ok, "product_catalog_service get_product_by_id response status not OK"
    response_json = response.json()
    price = response_json["price_usd"]
    return Product(
        product_id=response_json["id"],
        name=response_json["name"],
        description=response_json["description"],
        picture_url=response_json["picture"],
        categories=response_json.get("categories", []),
        price=ProductPrice(
            currency_code=price["currency_code"],
            units=price["units"],
            nanos=price["nanos"],
        ),
    )
