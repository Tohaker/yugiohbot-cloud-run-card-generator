import socket
import unittest

import pytest
from testfixtures import log_capture

from utils import gcsutils

if socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect_ex(('127.0.0.1', 4443)) != 0:
    pytest.skip("No GCS server running.", allow_module_level=True)


class TestGCSUtils(unittest.TestCase):
    @log_capture()
    def test_upload_card_valid(capture):
        file = "data/yugiohbot-images/cropped/1.jpg"
        gcsutils.upload_card(file)
        capture.check(('root', 'DEBUG', 'File {} uploaded to {}.'.format(file, file)))

    @log_capture()
    def test_download_image_valid(capture):
        file = 'cropped/1.jpg'
        dest = '1.jpg'
        gcsutils.download_image(file, dest)
        capture.check(('root', 'DEBUG', 'Blob {} downloaded to {}.'.format(file, dest)))

    def test_list_files_valid_bucket(self):
        bucket = 'yugiohbot-images'
        list = gcsutils.list_files_in_bucket(bucket)
        self.assertTrue(len(list) > 0)

    def test_list_files_invalid_bucket(self):
        bucket = 'wrong'
        list = gcsutils.list_files_in_bucket(bucket)
        self.assertTrue(len(list) == 0)


if __name__ == '__main__':
    unittest.main()
