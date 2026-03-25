import allure
import pytest
from assertpy import assert_that

from services.product_catalog_service.product_catalog_service import get_product_by_id
from services.product_catalog_service.product_catalog_service_models import GetProductByIdRequest


@allure.parent_suite("Services Tests")
@allure.suite("Product Catalog Service")
@allure.sub_suite("get product by id real target")
@pytest.mark.services_test
@pytest.mark.product_catalog_service
@pytest.mark.real_target
class TestGetProductByIdRealTarget:
    def test_get_product_by_id_against_real_target(self, real_product_catalog_config):
        request = GetProductByIdRequest(product_id=real_product_catalog_config.default_product_id)

        result = get_product_by_id(config=real_product_catalog_config, request=request)

        assert_that(result.product_id).is_equal_to(request.product_id)
        assert_that(result.name).is_not_empty()
        assert_that(result.description).is_not_empty()
        assert_that(result.categories).is_not_empty()
        assert_that(result.price.currency_code).is_equal_to("USD")
