
from django.shortcuts import render
from django.http import HttpResponse
from google.cloud import storage
import os
import posixpath
from PIL import Image


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def download_blob():
    """Downloads a blob from the bucket."""
    bucket_name = "image-processing-module.appspot.com"
    background_source_blob_name = "input_images/harry_potter.jpg"
    item_source_blob_name = "items/glasses1.png"

    print(BASE_DIR)
    bg_destination_file_name = os.path.join(BASE_DIR, "static_files/face_images/background_image.jpg")
    item_destination_file_name = os.path.join(BASE_DIR, "static_files/items/item1.png")


    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    # Construct a client side representation of a blob.
    # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
    # any content from Google Cloud Storage. As we don't need additional data,
    # using `Bucket.blob` is preferred here.
    BG_blob = bucket.blob(background_source_blob_name)
    BG_blob.download_to_filename(bg_destination_file_name)

    item_blob = bucket.blob(item_source_blob_name)
    item_blob.download_to_filename(item_destination_file_name)

    print(
        "Blob {} downloaded to {}.".format(
            background_source_blob_name, bg_destination_file_name
        )
    )

# create combines the background image (containing faces) with items (mask, glasses etc.)
def create(*args, **kwargs):

    download_blob()

    print(*args)
    bg_destination_file_name = os.path.join(BASE_DIR, "imageCreator/face_images/downloadedFile.jpg")
    path = "F:\ImageProcessingModule\ImageProcessingModule\ImageProcessingModule\imageCreator\face_images\downloadedFile.jpg"


    html = "<html><body><h1>IMAGE: </h1><img src= '/static/face_images/background_image.jpg' > <img src= '/static/items/item1.png' ></body></html>"

    return HttpResponse(html)


