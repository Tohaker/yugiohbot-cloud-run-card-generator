import os
import socket
import unittest

import pytest

from utils import gcsutils

if socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect_ex(('127.0.0.1', 4443)) != 0:
    pytest.skip("No GCS server running.", allow_module_level=True)


class TestGCSUtils(unittest.TestCase):

    def test_download_image_valid(self):
        file = 'cropped/1.jpg'
        dest = '1.jpg'
        storage_client = gcsutils.create_storage_client(True)
        gcsutils.download_image(file, dest, storage_client)
        self.assertTrue(os.path.exists(dest))
        os.remove(dest)

    def test_list_files_valid_bucket(self):
        bucket = 'yugiohbot-images'
        storage_client = gcsutils.create_storage_client(True)
        list = gcsutils.list_files_in_bucket(bucket, storage_client)
        self.assertTrue(len(list) > 0)

    def test_list_files_invalid_bucket(self):
        bucket = 'wrong'
        storage_client = gcsutils.create_storage_client(True)
        list = gcsutils.list_files_in_bucket(bucket, storage_client)
        self.assertTrue(len(list) == 0)


if __name__ == '__main__':
    unittest.main()
