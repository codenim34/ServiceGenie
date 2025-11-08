"""
In-memory database for prototype
"""
from typing import Dict, List
from datetime import datetime

class MemoryDB:
    def __init__(self):
        self.products: Dict[str, dict] = {}
        self.users: Dict[str, dict] = {}
        self.orders: Dict[str, dict] = {}
        self._counter = 0

    def _generate_id(self) -> str:
        self._counter += 1
        return str(self._counter)

    # Product methods
    def create_product(self, product_data: dict) -> dict:
        product_id = self._generate_id()
        product_data["id"] = product_id
        product_data["created_at"] = datetime.utcnow()
        product_data["updated_at"] = datetime.utcnow()
        self.products[product_id] = product_data
        return product_data

    def get_product(self, product_id: str) -> dict:
        return self.products.get(product_id)

    def list_products(self) -> List[dict]:
        return list(self.products.values())

    def update_product(self, product_id: str, product_data: dict) -> dict:
        if product_id in self.products:
            product_data["id"] = product_id
            product_data["updated_at"] = datetime.utcnow()
            self.products[product_id] = {**self.products[product_id], **product_data}
            return self.products[product_id]
        return None

    def delete_product(self, product_id: str) -> bool:
        if product_id in self.products:
            del self.products[product_id]
            return True
        return False

    # User methods
    def create_user(self, user_data: dict) -> dict:
        user_id = self._generate_id()
        user_data["id"] = user_id
        user_data["created_at"] = datetime.utcnow()
        self.users[user_id] = user_data
        return user_data

    def get_user(self, user_id: str) -> dict:
        return self.users.get(user_id)

    def get_user_by_email(self, email: str) -> dict:
        for user in self.users.values():
            if user["email"] == email:
                return user
        return None

    # Order methods
    def create_order(self, order_data: dict) -> dict:
        order_id = self._generate_id()
        order_data["id"] = order_id
        order_data["created_at"] = datetime.utcnow()
        order_data["status"] = "pending"
        self.orders[order_id] = order_data
        return order_data

    def get_order(self, order_id: str) -> dict:
        return self.orders.get(order_id)

    def list_user_orders(self, user_id: str) -> List[dict]:
        return [order for order in self.orders.values() if order["user_id"] == user_id]

# Create a global instance
db = MemoryDB()