from __future__ import annotations
from pydantic import BaseModel
from typing import List
from resources.rest_models import Link

class ProductModel(BaseModel):
    ProductID: int
    Name: str
    Category: str # Coffee, Dessert
    Price: float
    Threshold: int
    Quantity: int


model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "ProductID": 1,
                    "Name": "Cheesecake",
                    "Category": "Dessert",
                    "Price": 19.99,
                    "Threshold": 3,
                    "Quantity": 5
                }
            ]
        }
    }


class ProductRspModel(ProductModel):
    links: List[Link] = None



