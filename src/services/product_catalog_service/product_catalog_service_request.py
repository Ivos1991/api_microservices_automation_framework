from __future__ import annotations

from services.product_catalog_service.product_catalog_service_models import GetProductByIdRequest


class ProductCatalogServiceRequest:
    @staticmethod
    def get_product_by_id_request(request: GetProductByIdRequest) -> dict:
        return {"product_id": request.product_id}
