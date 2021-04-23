
from django.shortcuts import render
from django.http import HttpResponse
from google.cloud import storage
import os
import posixpath

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def download_blob():
    """Downloads a blob from the bucket."""
    bucket_name = "image-processing-module.appspot.com"
    source_blob_name = "input_images/harry_potter.jpg"
    destination_file_name = os.path.join(BASE_DIR, "imageCreator/face_images/downloadedFile.jpg")
    
    print(BASE_DIR)
    destination_file_name = os.path.join(BASE_DIR, "static_files/face_images/downloadedFile.jpg")

    #destination_file_name = os.path.join("/static", "downloadedFile.jpg")
    #destination_file_name = os.path.join(BASE_DIR, "face_images\downloadedFile.jpg")

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    # Construct a client side representation of a blob.
    # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
    # any content from Google Cloud Storage. As we don't need additional data,
    # using `Bucket.blob` is preferred here.
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    print(
        "Blob {} downloaded to {}.".format(
            source_blob_name, destination_file_name
        )
    )

# create combines the background image (containing faces) with items (mask, glasses etc.)
def create(*args, **kwargs):

    download_blob()

    print(*args)
    destination_file_name = os.path.join(BASE_DIR, "imageCreator/face_images/downloadedFile.jpg")
    path = "F:\ImageProcessingModule\ImageProcessingModule\ImageProcessingModule\imageCreator\face_images\downloadedFile.jpg"


    html = "<html><body><h1>IMAGE: </h1><img src= '/static/face_images/downloadedFile.jpg' ></body></html>"

    return HttpResponse(html)


