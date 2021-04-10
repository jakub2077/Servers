import unittest
from collections import Counter

from servers import ListServer, Product, Client, MapServer,TooManyProductsFoundError

server_types = (ListServer, MapServer)


class ListServerTest(unittest.TestCase):

    def test_get_entries_returned_list_sorted(self):
        products = [Product('Pa12', 1), Product('Ps23', 2), Product('Pd235', 1)]
        server = ListServer(products)
        entries = server.get_entries(2)
        self.assertEqual(entries, [products[0], products[2], products[1]])

    def test_error_throw(self):
        products = [Product('QWE211', 1), Product('qWE213', 2), Product('AQS21', 3), Product('VCS21', 4)]
        server = ListServer(products)
        with self.assertRaises(TooManyProductsFoundError):
            entries = server.get_entries(3)


class MapServerTest(unittest.TestCase):

    def test_get_entries_returned_map_sorted(self):
        products = [Product('Pa12',1), Product('Ps23',2), Product('Pd235',1)]
        server = MapServer(products)
        entries = server.get_entries(2)
        self.assertEqual(entries, [products[0], products[2], products[1]])

    def test_error_throw(self):
        products = [Product('QWE21', 1), Product('qWE21', 2), Product('AQS22', 3), Product('VCS21', 4),
                    Product('QWS45', 5)]
        server = MapServer(products)
        with self.assertRaises(TooManyProductsFoundError):
            entries = server.get_entries(3)


class ServerTest(unittest.TestCase):

    def test_get_entries_returns_proper_entries(self):
        products = [Product('P12', 1), Product('PP234', 2), Product('PP235', 1)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)
            self.assertEqual(Counter([products[2], products[1]]), Counter(entries))


class ClientTest(unittest.TestCase):
    def test_total_price_for_normal_execution(self):
        products = [Product('PP234', 2), Product('PP235', 3)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(5, client.get_total_price(2))

    def test_total_price_for_no_entries_found(self):
        products = [Product('QWE21', 1), Product('qWE21', 2), Product('AQS22', 3), Product('VCS21', 4),
                    Product('QWS45', 5)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(None, client.get_total_price(2))

    def test_total_price_for_exception_thrown(self):
        products = [Product('QWE21', 1), Product('qWE21', 2), Product('AQS22', 3), Product('VCS21', 4),
                    Product('QWS45', 5)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            with self.assertRaises(TooManyProductsFoundError):
                entries=server.get_entries(3)
                self.assertEqual(None, client.get_total_price(3))


if __name__ == '__main__':
    unittest.main()
