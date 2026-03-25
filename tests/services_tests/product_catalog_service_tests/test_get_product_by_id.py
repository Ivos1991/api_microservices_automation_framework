import allure
import pytest
from assertpy import assert_that

from services.product_catalog_service.product_catalog_service import get_product_by_id


@allure.parent_suite("Services Tests")
@allure.suite("Product Catalog Service")
@allure.sub_suite("get product by id")
@pytest.mark.services_test
@pytest.mark.product_catalog_service
class TestGetProductById:
    def test_get_product_by_id_returns_expected_product(self, config, product_lookup_request):
        result = get_product_by_id(config=config, request=product_lookup_request)

        assert_that(result.product_id).is_equal_to(product_lookup_request.product_id)
        assert_that(result.name).is_not_empty()
        assert_that(result.picture_url).contains("http")
        assert_that(result.categories).is_not_empty()
        assert_that(result.price.currency_code).is_equal_to("USD")
