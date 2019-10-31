import logging

from google.cloud import storage

storage_client = storage.Client()


def upload_card(file):
    bucket_name = "generated-cards"
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(file)
    with open(file, 'rb') as card_file:
        blob.upload_from_file(card_file)
    logging.debug("File {} uploaded to {}.".format(file, file))


def download_image(file, destination):
    bucket_name = "yugiohbot-images"
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(file)
    blob.download_to_filename(destination)  # Remove the pathname from the image so we can save it.
    logging.debug('Blob {} downloaded to {}.'.format(file, destination))


def list_files_in_bucket(bucket):
    file_list = list(storage_client.list_blobs(bucket, prefix='cropped'))
    return file_list
