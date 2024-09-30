import xmlrpc.client
from unittest import TestCase

from calculator import Calculator


class TestXMLCalculator(TestCase):

    def setUp(self):
        self.client = xmlrpc.client.ServerProxy(f"http://127.0.0.1:8000/")

    def test_connection(self):
        response = self.client.ping()
        self.assertEqual(response, 'pong')

    def test_add(self):
        x, y = 1., 2.
        expected = Calculator.add(x, y)
        result = self.client.add(x, y)
        self.assertAlmostEqual(expected, result, places=1)

    def test_subtract(self):
        x, y = 1., 2.
        expected = Calculator.subtract(x, y)
        result = self.client.subtract(x, y)
        self.assertAlmostEqual(expected, result, places=1)

    def test_multiply(self):
        x, y = 1., 2.
        expected = Calculator.multiply(x, y)
        result = self.client.multiply(x, y)
        self.assertAlmostEqual(expected, result, places=1)

    def test_divide(self):
        x, y = 1., 2.
        expected = Calculator.divide(x, y)
        result = self.client.divide(x, y)
        self.assertAlmostEqual(expected, result, places=1)

    def test_sqrt(self):
        x = 4.
        expected = Calculator.sqrt(x)
        result = self.client.sqrt(x)
        self.assertAlmostEqual(expected, result, places=1)

    def test_round(self):
        x, digit = 4.5123123, 2
        expected = Calculator.round(x, digit)
        result = self.client.round(x, digit)
        self.assertAlmostEqual(expected, result, places=1)

    def test_pow(self):
        x, y = 2., 3
        expected = Calculator.pow(x, y)
        result = self.client.pow(x, y)
        self.assertAlmostEqual(expected, result, places=1)

    def test_multiple_call_operations(self):
        expected = 538.
        multi = xmlrpc.client.MultiCall(self.client)
        multi.add(1., 2.)
        multi.subtract(5., 2.)
        multi.pow(2., 9)
        multi.multiply(10., 2.)

        result = 0.
        for response in multi():
            result += response

        self.assertAlmostEqual(expected, result, places=1)
