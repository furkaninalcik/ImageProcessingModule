"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask , request
from flask import render_template
from PIL import Image

import create_image

app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
#wsgi_app = app.wsgi_app


@app.route('/')
def hello():
    """Renders a sample page."""
    return "Welcome to the Image Processing Module developed with Flask - Python"


@app.route('/create_image', methods=['POST'])
def image_creation():
    """Combines images"""
    #faceAnnotations = request.args.get("faceAnnotations")
    #faceAnnotations = request.args["faceAnnotations"]
    faceAnnotations = request.get_json()
    print('FACE 0 : ')
    print(faceAnnotations['face0'])

    

    return  create_image.create(faceAnnotations)
    
    #return render_template('index.html')
    #return "Welcome to the Image Processing Module developed with Flask - Python"


if __name__ == '__main__':
    app.run(debug=True)