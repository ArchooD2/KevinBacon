
import unittest
from baconwaffle import find_shortest_path as your_function_name

class TestBaconWaffle(unittest.TestCase):
    def test_function_name(self):
        start = "Python (programming language)"
        result = your_function_name("Python (programming language)")
        print(result)
        midrim = result[0] == start and result[-1] == "Kevin Bacon"
        self.assertEqual(midrim, True)

if __name__ == '__main__':
    unittest.main()
