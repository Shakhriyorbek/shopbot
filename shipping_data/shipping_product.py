from dataclasses import dataclass
from typing import List
from telebot.types import LabeledPrice

@dataclass
class Product:
    title: str
    description: str
    start_parameter: str
    currency: str
    prices: List[LabeledPrice]
    provider_token: str
    provider_data: dict = None
    need_name: bool = False

    def generate_invoice(self):
        return self.__dict__

