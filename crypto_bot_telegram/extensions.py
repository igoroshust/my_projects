import requests
import json
from config import exchanges

class ApiException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            return ApiException(f"Валюта {base} не найдена.")
        try:
            sym_key = exchanges[sym.lower()]
        except KeyError:
            raise ApiException(f"Валюта {sym} не найдена")

        if base_key == sym_key:
            raise ApiException(f"Невозможно перевести одинаковые валюты")

        try:
            amount = float(amount.replace(',', '.'))
        except ValueError:
            raise ApiException(f"Не удалось обработать количество: {amount}")

        r = requests.get(f"https://api.getgeoapi.com/v2/currency/convert?api_key=3a4f9408660282f7aae6efb737c70d47ee000f33&from={base_key}&to={sym_key}&amount={amount}")
        resp = json.loads(r.content)  # парсим строку в объект
        new_price = float(resp['rates'][sym_key]['rate_for_amount'])
        return round(new_price, 2)