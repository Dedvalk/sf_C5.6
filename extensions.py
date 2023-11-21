import requests
from config import URL, DATA

class Converter:
    @staticmethod
    def get_price(source, dest, volume):
        base = DATA.get(source)
        if not base:
            raise APIException('Некорректно указана исходная валюта')
        quote = DATA.get(dest)
        if not quote:
            raise APIException('Некорректно указана целевая валюта')
        try:
            amount = float(volume)
        except ValueError:
            raise APIException('Некорректно указано количество')

        data = {'fsym': base, 'tsyms': quote}
        req = requests.get(URL, params=data).json()
        return float(req[quote])*amount

    @staticmethod
    def send_req(base, quote):
        data = {'fsym': base, 'tsyms': quote}
        req = requests.get(URL, params=data).json()
        return req[quote]

class APIException(Exception):
    pass
