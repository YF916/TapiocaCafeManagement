from resources.abstract_base_resource import BaseResource
from resources.products.product_models import ProductModel, ProductRspModel
from resources.rest_models import Link
from typing import List


class ProductsResource(BaseResource):
    def __init__(self, config):
        super().__init__()

        self.data_service = config["data_service"]

    @staticmethod
    def _generate_links(s: dict) -> ProductRspModel:

        self_link = Link(**{
            "rel": "self",
            "href": "/products/" + str(s['ProductID'])
        })

        links = [
            self_link,
        ]
        rsp = ProductRspModel(**s, links=links)
        return rsp

    def get_products(self, ProductID: int = None) -> List[ProductRspModel]:

        result = self.data_service.get_products(ProductID)
        final_result = []

        for s in result:
            m = self._generate_links(s)
            final_result.append(m)

        return final_result

    def create_product(self, Name: str, Category: str, Price: float, Threshold: int, Quantity: int):

        result = self.data_service.create_product(Name=Name, Category=Category, Price=Price, Threshold=Threshold, Quantity=Quantity)
        return result
        #if type(result) == str:
        #    return result
        #final_result = self._generate_links(result)

        #return final_result

    def change_quantity(self, ProductID: int, num: int):
        result = self.data_service.change_quantity(ProductID=ProductID, num=num)
        return result
        # if type(result) == str:
        #     return result
        # final_result = self._generate_links(result)
        # return final_result

    def change_price(self, ProductID: int, new_price: float):
        result = self.data_service.change_price(ProductID=ProductID, new_price=new_price)
        return result
        # if type(result) == str:
        #     return result
        # final_result = self._generate_links(result)
        # return final_result

    def delete_product(self, ProductID: int):
        result = self.data_service.delete_product(ProductID=ProductID)
        return result
