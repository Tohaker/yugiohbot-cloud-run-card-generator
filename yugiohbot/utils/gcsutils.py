import logging

import requests
import urllib3
from google.api_core.client_options import ClientOptions
from google.api_core.exceptions import NotFound
from google.auth.credentials import AnonymousCredentials
from google.cloud import storage


def create_storage_client(test):
    if test:
        EXTERNAL_URL = "https://127.0.0.1:4443"
        PUBLIC_HOST = "storage.gcs.127.0.0.1.nip.io:4443"

        storage.blob._API_ACCESS_ENDPOINT = "https://" + PUBLIC_HOST
        storage.blob._DOWNLOAD_URL_TEMPLATE = (
                u"%s/download/storage/v1{path}?alt=media" % EXTERNAL_URL
        )
        storage.blob._BASE_UPLOAD_TEMPLATE = (
                u"%s/upload/storage/v1{bucket_path}/o?uploadType=" % EXTERNAL_URL
        )
        storage.blob._MULTIPART_URL_TEMPLATE = storage.blob._BASE_UPLOAD_TEMPLATE + u"multipart"
        storage.blob._RESUMABLE_URL_TEMPLATE = storage.blob._BASE_UPLOAD_TEMPLATE + u"resumable"

        my_http = requests.Session()
        my_http.verify = False  # disable SSL validation
        urllib3.disable_warnings(
            urllib3.exceptions.InsecureRequestWarning
        )  # disable https warnings for https insecure certs

        storage_client = storage.Client(
            credentials=AnonymousCredentials(),
            project="test",
            _http=my_http,
            client_options=ClientOptions(api_endpoint=EXTERNAL_URL),
        )
    else:
        storage_client = storage.Client()

    return storage_client


def upload_card(file, storage_client):
    bucket_name = "generated-cards"
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(file)
    with open(file, 'rb') as card_file:
        blob.upload_from_file(card_file)
    logging.debug("File {} uploaded to {}.".format(file, file))


def download_image(file, destination, storage_client):
    bucket_name = "yugiohbot-images"
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(file)
    blob.download_to_filename(destination)  # Remove the pathname from the image so we can save it.
    logging.debug('Blob {} downloaded to {}.'.format(file, destination))


def list_files_in_bucket(bucket, prefix, storage_client):
    file_list = []
    try:
        file_list = list(storage_client.list_blobs(bucket, prefix=prefix))
    except NotFound as e:
        logging.debug('Could not find bucket {}: {}'.format(bucket, e))

    return file_list
