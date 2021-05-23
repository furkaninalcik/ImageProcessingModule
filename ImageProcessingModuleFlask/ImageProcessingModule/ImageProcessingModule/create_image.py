
#from django.shortcuts import render
#from django.http import HttpResponse
from google.cloud import storage
import os
import posixpath
import math
import requests

from PIL import Image

from flask import Flask  , jsonify
from flask import render_template
from flask import current_app


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
Static_Directory_Path = Flask.static_folder

print("PATH :" + BASE_DIR)

def download_blob(bucket_name, background_source_blob_name,  item_source_blob_name):
    """Downloads a blob from the bucket."""



    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    # Construct a client side representation of a blob.
    # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
    # any content from Google Cloud Storage. As we don't need additional data,
    # using `Bucket.blob` is preferred here.
    BG_blob = bucket.blob(background_source_blob_name)
    BG_blob.download_to_filename("/tmp/bg_destination_file_name")

    item_blob = bucket.blob(item_source_blob_name)
    item_blob.download_to_filename("/tmp/item_destination_file_name")

    #combine_tmp_images(faceAnnotations)

    #print(
    #    "Blob {} downloaded to {}.".format(
    #        background_source_blob_name, bg_destination_file_name
    #    )
    #)



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

    #blob.upload_from_filename(source_file_name)
    blob.upload_from_filename("/tmp/final_image_directory.jpg")

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )



# create() combines the background image (containing faces) with items (hats, glasses etc.)
def create(disguise_request):

    upload_bucket_name = "image-processing-module.appspot.com"
    bucket_name = disguise_request['bucket_name']
    #background_source_blob_name = "input_images/The_Traitorous_Eight.jpeg"
    background_source_blob_name = disguise_request['image_file_name']
    #item_source_blob_name = "items/glasses0.png"
    item_source_blob_name = disguise_request['faces'][0]['item_file_name']

    #bg_destination_file_name = os.path.join(BASE_DIR, "tmp/static/face_images/background_image.jpg")
    #item_destination_file_name = os.path.join(BASE_DIR, "static/items/item1.png")

    final_image_directory = os.path.join(BASE_DIR, "static/output_images/final.png")
    destination_blob_name = "output_images/final_" + background_source_blob_name + ".jpeg"
    
    
    download_blob(bucket_name, background_source_blob_name,  item_source_blob_name)


    combine_tmp_images(disguise_request)

    #combine_images(item_destination_file_name , bg_destination_file_name , final_image_directory)

    upload_blob(upload_bucket_name, final_image_directory, destination_blob_name)

    return bucket_name + "/" + destination_blob_name
 

    # send the output image url to the manager service
    #url = 'https://www.w3schools.com/python/demopage.php'
    #myobj = {'somekey': 'somevalue'}

    #x = requests.post(url, data = myobj)

    #print(x.text)


    #print(*args)
    #bg_destination_file_name = os.path.join(BASE_DIR, "imageCreator/face_images/downloadedFile.jpg")
    #path = "F:\ImageProcessingModule\ImageProcessingModule\ImageProcessingModule\imageCreator\face_images\downloadedFile.jpg"


    #html = "<html><body><h1>IMAGE: </h1><img src= '/static/face_images/background_image.jpg' > <img src= '/static/items/item1.png' ></body></html>"

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
def vector_length(v):
    return math.sqrt(v[0]*v[0] + v[1]*v[1])



def combine_tmp_images(diguise_request):

    bg = Image.open("/tmp/bg_destination_file_name")
    item = Image.open("/tmp/item_destination_file_name")

    back_im = bg.copy()

    




    lefteye = diguise_request['faces'][0]['detection']['lefteye']
    midpoint = diguise_request['faces'][0]['detection']['midpoint']
    rigtheye = diguise_request['faces'][0]['detection']['righteye']


    #for face in faceAnnotations:
        
    """lefteye = faceAnnotations[face]['lefteye']

    midpoint = faceAnnotations[face]['midpoint']
    rigtheye = faceAnnotations[face]['rigtheye']"""

    item_rotation = (rigtheye['y'] - lefteye['y'] ) / (rigtheye['x'] - lefteye['x'] )
    eyes_vector =  (rigtheye['x'] - lefteye['x'] , rigtheye['y'] - lefteye['y'] )  # the 2d vector from left eye to right eye
    
    print("eyes_vector: ")
    print(eyes_vector)

    print("item.size: ")
    print(item.size)

    coef = vector_length(eyes_vector) / vector_length(item.size)
    coef *= 2 # this constant is determined experimentally 
    print("coef: ")
    print(coef)

    new_item_size = (int(item.size[0] * coef) , int(item.size[1] * coef)  )

    print("new_item_size: ")
    print(new_item_size)
    #item_rotation = 20

    #faceAnnotations.x = 260
    #faceAnnotations.y = 340
    #faceAnnotations = jsonify(faceAnnotations)


    item = item.resize(new_item_size).rotate(int(item_rotation), expand = True)

    x_coordinate = int(midpoint['x'] - item.size[0] / 2)
    y_coordinate = int(midpoint['y'] - item.size[1] / 2)

    back_im.paste(item, (x_coordinate, y_coordinate) , item)

    #back_im.show()
    back_im.save("/tmp/final_image_directory.jpg", quality=95)