#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Optional, List, Dict
from abc import ABC, abstractmethod
import re


class Product:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą argumenty wyrażające nazwę produktu (typu str) i jego cenę (typu float)
    #  -- w takiej kolejności -- i ustawiającą atrybuty `name` (typu str) oraz `price` (typu float)

    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    def __hash__(self):
        return hash((self.name, self.price))

    def __eq__(self, other):
        return self.name == other.name and self.price == other.price


class ServerError(Exception):
    pass


class TooManyProductsFoundError(ServerError):
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.

    def __init__(self, massage: str = 'Too many products found'):
        super().__init__()
        self.massage = massage

# FIXME: Każada z poniższych klas serwerów powinna posiadać:
#  (1) metodę inicjalizacyjną przyjmującą listę obiektów typu `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#  (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną dopuszczalną liczbę wyników wyszukiwania,
#  (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów spełniających kryterium wyszukiwania


class Server(ABC):

    n_max_returned_entries: int = 3

    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_entries(self, n_letters: int) -> List[Product]:
        pass


class ListServer(Server):

    def __init__(self, products: List[Product]):
        super().__init__()
        self.products = products

    def get_entries(self, n_letters: int) -> List[Product]:
        result = list()
        for product in self.products:
            criteria = re.match('^[a-zA-Z]{{{n}}}\\d{{2,3}}$'.format(n=n_letters), product.name)
            if criteria:
                if len(result) < self.n_max_returned_entries:
                    result.append(product)
                else:
                    raise TooManyProductsFoundError
        if result:
            data = result[:]
            n = len(data)
            update = 1
            while update == 1 and n > 1:
                update = 0
                for i in range(len(data) - 1):
                    if data[i].price > data[i + 1].price:
                        data[i], data[i + 1] = data[i + 1], data[i]
                        update = 1
                if update == 0:
                    break
            n -= 1
            result = data[:]

        return result if result else []


class MapServer(Server):

    def __init__(self, products: List[Product]):
        super().__init__()
        self.products = {}
        for e in products:
            self.products[e.name] = e

    def get_entries(self, n_letters: int) -> List[Product]:
        result = list()
        for product in self.products.values():
            criteria = re.match('^[a-zA-Z]{{{n}}}\\d{{2,3}}$'.format(n=n_letters), product.name)
            if criteria:
                if len(result) < self.n_max_returned_entries:
                    result.append(product)
                else:
                    raise TooManyProductsFoundError
        if result:
            data = result[:]
            n = len(data)
            update = 1
            while update == 1 and n > 1:
                update = 0
                for i in range(len(data)-1):
                    if data[i].price > data[i+1].price:
                        data[i], data[i+1] = data[i+1], data[i]
                        update = 1
                if update == 0:
                    break
            n -= 1
            result = data[:]
        return result if result else []


class Client(object):
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer

    def __init__(self, server: Server):
        self.server = server

    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        total_price = float(0)
        result = self.server.get_entries(n_letters)
        for product in result:
            total_price += product.price
        if self.server.get_entries(n_letters) == TooManyProductsFoundError:
            return None
        if total_price == 0:
            return None
        else:
            return total_price
