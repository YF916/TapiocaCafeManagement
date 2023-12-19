import pytest
from unittest.mock import MagicMock
from resources.products.product_models import ProductModel, ProductRspModel
from resources.products.products_resource import ProductsResource

@pytest.fixture
def mock_data_service():
    return MagicMock()

@pytest.fixture
def products_resource(mock_data_service):
    config = {"data_service": mock_data_service}
    return ProductsResource(config)

def test_get_products_no_id(products_resource, mock_data_service):
    # Update the mock return value to include all necessary fields
    mock_data_service.get_products.return_value = [
        {
            'ProductID': 1,
            'Name': 'Test Product',
            'Category': 'Test Category',
            'Price': 100.0,
            'Threshold': 10,
            'Quantity': 5
        }
    ]
    products = products_resource.get_products()
    assert len(products) == 1
    assert isinstance(products[0], ProductRspModel)
    mock_data_service.get_products.assert_called_once_with(None)


def test_get_products_with_id(products_resource, mock_data_service):
    ProductID = 1
    mock_data_service.get_products.return_value = [
        {
            'ProductID': ProductID,
            'Name': 'Test Product',
            'Category': 'Test Category',
            'Price': 100.0,
            'Threshold': 10,
            'Quantity': 5
        }
    ]
    products = products_resource.get_products(ProductID)
    assert len(products) == 1
    assert products[0].ProductID == ProductID
    mock_data_service.get_products.assert_called_once_with(ProductID)


def test_create_product(products_resource, mock_data_service):
    mock_data_service.create_product.return_value = 'New Product Created!'
    result = products_resource.create_product("Test", "Category", 100.0, 10, 5)
    assert result == 'New Product Created!'
    mock_data_service.create_product.assert_called_once()


# Add tests for change_quantity, change_price, and delete_product methods

