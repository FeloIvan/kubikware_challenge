import unittest
from main import process_census_data


class TestProcess(unittest.TestCase):

 
    def test_dict(self):
        url = "https://www2.census.gov/geo/docs/reference/codes2020/national_county2020.txt"
        self.dict_data = process_census_data(url)
        self.assertTrue(type(self.dict_data) is dict)

if __name__ == '__main__':
    unittest.main()