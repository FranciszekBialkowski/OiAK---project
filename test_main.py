import unittest
import random

from main import check_if_modulo_is_valid, preprocessing, \
    calculate_bits, decimal_to_binary

class Test(unittest.TestCase):

    def test_preprocessing(self):
        for i in range(1000):
            with self.subTest(i=i):
                modulo = random.randrange(5, 10000)

                while not check_if_modulo_is_valid(modulo):
                    modulo = random.randrange(5, 10000)

                A_dec = random.randrange(0, modulo-1)
                B_dec = random.randrange(0, modulo-1)
                expected_result = (A_dec + B_dec) % modulo

                n = calculate_bits(modulo)

                A = decimal_to_binary(A_dec,n)
                B = decimal_to_binary(B_dec,n)

                self.assertEqual(expected_result,
                                 preprocessing(n, modulo, A, B))
