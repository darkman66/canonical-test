import os
import unittest
from hashlib import md5
from mock import patch, Mock
from package_statistics import pretty_print_results
from package_statistics import top_list
from package_statistics import download_file


class TestPrettyPrint(unittest.TestCase):

    @patch('package_statistics.log.info')
    def test_valid_pretty_print_result(self, mock_info):
        data = [("a", "1"), ("b", 2)]
        pretty_print_results(data)
        self.assertEqual(mock_info.call_count, 3)
        self.assertEqual('No|packagename|numberoffiles', mock_info.call_args_list[0][0][0].replace(' ', ''))
        self.assertEqual('1|a|1', mock_info.call_args_list[1][0][0].replace(' ', ''))
        self.assertEqual('2|b|2', mock_info.call_args_list[2][0][0].replace(' ', ''))

    @patch('package_statistics.log.info')
    def test_empty_result(self, mock_info):
        data = []
        pretty_print_results(data)
        self.assertEqual(mock_info.call_count, 1)
        self.assertEqual('No|packagename|numberoffiles', mock_info.call_args_list[0][0][0].replace(' ', ''))

    @patch('package_statistics.log.info')
    def test_invalid_result(self, mock_info):
        data = None
        pretty_print_results(data)
        self.assertEqual(mock_info.call_count, 1)
        self.assertEqual('No|packagename|numberoffiles', mock_info.call_args_list[0][0][0].replace(' ', ''))


class TestSortingTopList(unittest.TestCase):

    def setUp(self):
        self.data = [("c", 20), ("a", 1), ("b", 2), ("z", 100)]

    def test_valid_data(self):
        result = top_list(self.data)
        self.assertEqual(result, [('z', 100), ('c', 20), ('b', 2), ('a', 1)])

    def test_valid_max_result(self):
        result = top_list(self.data, 1)
        self.assertEqual(result, [('z', 100)]) 

    def test_invalid_input(self):
        result = top_list(None)
        self.assertIsNone(result) 


class TestDownloadFile(unittest.TestCase):

    def setUp(self):
        self.url = 'http://foo.org'
        self.cache_file = '/var/tmp/{}'.format(md5(self.url.encode('latin-1')).hexdigest())
        if os.path.exists(self.cache_file):
            os.remove(self.cache_file)

    @patch('package_statistics.save_cache')
    @patch('package_statistics.requests.get')
    def test_calling_external_resource_when_no_cache_in_use(self, mock_get, mock_save):
        mock_get.return_result = Mock(content='abc')
        download_file(self.url)
        mock_get.assert_called_once_with(self.url, allow_redirects=True)
        mock_save.assert_not_called()

    @patch('package_statistics.options')
    @patch('package_statistics.save_cache')
    @patch('package_statistics.requests.get')
    def test_valid_cache_save(self, mock_get, mock_save, mock_options):
        downloaded_value = 'some text'
        mock_get.return_value = Mock(content=downloaded_value)
        mock_options.return_value = Mock(cache=True)
        result = download_file(self.url)
        mock_get.assert_called_once_with(self.url, allow_redirects=True)
        mock_save.assert_called_once_with(self.cache_file)
        self.assertEqual(result, downloaded_value)

    @patch('package_statistics.options')
    @patch('package_statistics.save_cache')
    @patch('package_statistics.requests.get')
    def test_valid_cache_load(self, mock_get, mock_save, mock_options):
        cached_value = b'lalalasdkjfksdhfksdjfh'
        open(self.cache_file, 'wb').write(cached_value)
        mock_get.return_result = Mock(content='abc')
        mock_options.return_value = Mock(cache=True)
        result = download_file(self.url)
        mock_get.assert_not_called()
        mock_save.assert_not_called()

        self.assertEqual(result, cached_value)
