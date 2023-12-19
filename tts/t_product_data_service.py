import pytest
from decimal import Decimal
from unittest.mock import MagicMock
from resources.products.products_data_service import ProductDataService

@pytest.fixture
def mock_db_connection():
    return MagicMock()

@pytest.fixture
def product_service(mock_db_connection):
    config = {"db_connection": mock_db_connection}
    return ProductDataService(config)

def test_get_products_no_id(product_service, mock_db_connection):
    mock_db_connection.cursor.return_value.fetchall.return_value = []
    result = product_service.get_products()
    assert result == []
    mock_db_connection.cursor.return_value.execute.assert_called_once()

def test_get_products_with_id(product_service, mock_db_connection):
    ProductID = 1
    mock_db_connection.cursor.return_value.fetchall.return_value = []
    result = product_service.get_products(ProductID)
    assert result == []
    mock_db_connection.cursor.return_value.execute.assert_called_once_with(
        """SELECT * FROM Product WHERE ProductID=%s;""", (ProductID,))

def test_create_product(product_service, mock_db_connection):
    result = product_service.create_product("Test", "Category", Decimal('100.0'), 10, 5)
    assert result == "New Product Created!"
    mock_db_connection.cursor.return_value.execute.assert_called_once()

# Add tests for change_quantity, change_price, and delete_product methods

