
#from django.shortcuts import render
#from django.http import HttpResponse
from google.cloud import storage
import os
import posixpath
from PIL import Image

from flask import render_template


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def download_blob(bucket_name, background_source_blob_name,  item_source_blob_name, bg_destination_file_name , item_destination_file_name):
    """Downloads a blob from the bucket."""



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



def upload_blob(bucket_name, source_file_name, destination_blob_name):

    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )



# create combines the background image (containing faces) with items (mask, glasses etc.)
def create():

    bucket_name = "image-processing-module.appspot.com"
    background_source_blob_name = "input_images/harry_potter.jpg"
    item_source_blob_name = "items/glasses1.png"

    bg_destination_file_name = os.path.join(BASE_DIR, "ImageProcessingModule/static/face_images/background_image.jpg")
    item_destination_file_name = os.path.join(BASE_DIR, "ImageProcessingModule/static/items/item1.png")

    final_image_directory = os.path.join(BASE_DIR, "ImageProcessingModule/static/output_images/final.png")
    destination_blob_name = "output_images/final_image.jpg"
    
    
    download_blob(bucket_name, background_source_blob_name,  item_source_blob_name, bg_destination_file_name , item_destination_file_name)

    combine_images(item_destination_file_name , bg_destination_file_name , final_image_directory)

    upload_blob(bucket_name, final_image_directory, destination_blob_name)




    #print(*args)
    #bg_destination_file_name = os.path.join(BASE_DIR, "imageCreator/face_images/downloadedFile.jpg")
    #path = "F:\ImageProcessingModule\ImageProcessingModule\ImageProcessingModule\imageCreator\face_images\downloadedFile.jpg"


    html = "<html><body><h1>IMAGE: </h1><img src= '/static/face_images/background_image.jpg' > <img src= '/static/items/item1.png' ></body></html>"

    #return HttpResponse(html)
    #return render_template('index.html')

def combine_images(item_image_path, bg_image_path, final_image_directory):

    bg = Image.open(bg_image_path)
    item = Image.open(item_image_path)
    new_item_size = (370, 125)
    item = item.resize(new_item_size).rotate(20, expand = True)
    back_im = bg.copy()
    back_im.paste(item, (260,340) , item)
    back_im.save(final_image_directory, quality=95)


    #return null