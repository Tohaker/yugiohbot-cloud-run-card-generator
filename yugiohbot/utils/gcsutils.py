from google.cloud import storage
import logging

storage_client = storage.Client()


def upload_card(file):
    bucket_name = "generated-cards"
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(file)
    with open(file, 'rb') as card_file:
        blob.upload_from_file(card_file)
    logging.debug("File {} uploaded to {}.".format(file, file))


def download_image(file):
    bucket_name = "yugiohbot-images"
    bucket = storage_client.get_bucket(bucket_name)
    file_path = 'cropped/' + file
    blob = bucket.blob(file_path)
    blob.download_to_filename(file)
    logging.debug('Blob {} downloaded to {}.'.format(file_path, file))
