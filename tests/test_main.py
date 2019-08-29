import unittest
from mock import patch
from package_statistics import pretty_print_results



class TestPrettyPrint(unittest.TestCase):

    @patch('package_statistics.log.info')
    def test_valid_pretty_print_result(self, mock_info):
        data = [("a", "1"), ("b", 2)]
        pretty_print_results(data)
        self.assertEqual(mock_info.call_count, 3)
        self.assertEqual('No|packagename|numberoffiles', mock_info.call_args_list[0][0][0].replace(' ', ''))
        self.assertEqual('1|a|1', mock_info.call_args_list[1][0][0].replace(' ', ''))
        self.assertEqual('2|b|2', mock_info.call_args_list[2][0][0].replace(' ', ''))

