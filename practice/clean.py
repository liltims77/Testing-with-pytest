#You have a function clean_data(data) that takes in a list of dictionaries representing records. 
# Write a unit test to ensure the function removes records with missing age fields.

# Function to be tested
def clean_data(data):
    return [record for record in data if 'age' in record and record['age'] is not None]


import unittest
class Testcleandata(unittest.TestCase):
    def test_clean_data(self):
        data = [
            {'name': 'Alice', 'age': 25},
            {'name': 'Tim', 'age': 20},
            {'name': 'Timzz'},
            {'name': 'faith', 'age': 25}
        ]

        cleaned_data = clean_data(data)
        expected_data = [{'name': 'Alice', 'age': 25}, {'name': 'Tim', 'age': 20}, {'name': 'faith', 'age': 25}]

        self.assertEqual(cleaned_data, expected_data)

if __name__ == '__main__':
    unittest.main()