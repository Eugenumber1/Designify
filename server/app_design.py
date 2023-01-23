import uuid
from flask import Flask, url_for, request, redirect, jsonify
from flask import render_template
from pyunsplash import PyUnsplash
from flask_cors import CORS
from cavlib import CAV
import urllib.request
import os
from pathlib import Path
from tqdm import tqdm



# configuration
DEBUG = True

# ------------ ATOMIC VARS ---------------


app = Flask(__name__)
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = 'you-will-never-guess'
api_key = 'mJpXOSabo4pvepg4JaPEOMhBWUxmS86hQIvueQQezx4'
app.config.from_object(__name__)
py_un = PyUnsplash(api_key=api_key)
CORS(app, resources={r'/*': {'origins': '*'}})


# ------------RESOURCES------------

PHOTOS = [
    # {
    #     'id': uuid.uuid4().hex,
    #     'word': 'Tadj Mahal',
    #     'url': ['https://unsplash.com/photos/S34fEzWT6eE/download?ixid=MnwzOTEwNTZ8MXwxfHNlYXJjaHwxfHxpbm5vdmF0aW9ufGVufDB8fHx8MTY3MzUyNjg5Mg']
    # },
    # {
    #     'id': uuid.uuid4().hex,
    #     'word': 'Something Else',
    #     'url': ['https://unsplash.com/photos/G7VN8NadjO0/download?ixid=MnwzOTEwNTZ8MHwxfHNlYXJjaHw3fHxpbm5vdmF0aW9ufGVufDB8fHx8MTY3MzUyNjg5Mg']
    # }
]

# --------------- API -------------------


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('Damn I did it')

@app.route('/photos', methods=['POST', 'GET'])  # url for my app
def home():
    response_object = {'status': 'success'}
    if request.method == "POST":
        post_data = request.get_json()
        word = post_data.get('word')
        search = py_un.search(type_='photos', per_page=15, query=word)
        photos = list()
        #print(type(search))
        for entry in search.entries:
            photos.append(entry.link_download)
            #print(entry.link_download)
        #print(len(photos))
        photo_object = dict()
        photo_object['id'] = uuid.uuid4().hex
        photo_object['word'] = word
        #print(photo_object['word'])
        photo_object['url'] = dict()
        parameter = 3
        for photo in photos:
            photo_object['url'][uuid.uuid4().hex] = [photo, parameter]
        response_object['photos'] = photo_object
        PHOTOS.append(photo_object)
        response_object['message'] = 'Photo added!'
        print(response_object)
        return jsonify(response_object)
    else:
        response_object['photos'] = PHOTOS
        return jsonify(response_object)

@app.route('/photos/<photo_object_id>/<photo_id>', methods=['PUT', 'DELETE'])
def single_photo(photo_object_id, photo_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        put_data = request.get_json()
        if update_photo(photo_object_id, photo_id, put_data.get('weight')):
            response_object['message'] = 'Weight was updated!'
    if request.method == 'DELETE':
        if remove_photo(photo_object_id, photo_id):
            response_object['message'] = 'Photo was deleted'
    return jsonify(response_object)


# update photo
def update_photo(photo_object_id, photo_id, weight):
    for photo_object in PHOTOS:
        if photo_object['id'] == photo_object_id:
            photo_object['url'][photo_id][1] = int(weight)
            return True
    return False

# remove photo
def remove_photo(photo_object_id, photo_id):
    for photo_object in PHOTOS:
        if photo_object['id'] == photo_object_id:
            photo_object['url'].pop(photo_id)
            return True
    return False

@app.route('/concept/<photo_object_id>', methods=['POST', 'DELETE'])
def concept(photo_object_id):
    response_object = {'status': 'success'}
    if request.method == 'POST':
        for photo_object in PHOTOS:
            if photo_object.get('id') == photo_object_id:
                parent = '/Users/zhenyabudnyk/PycharmProjects/Designify/unsplash_pics'
                directory = photo_object_id
                path = os.path.join(parent, directory)
                print(path)
                os.makedirs(path, exist_ok=True)
                print(path)
                for (key, value) in tqdm(photo_object.get('url').items()):
                     download_image(value[0], path, key)
                PHOTOS.remove(photo_object)
    if request.method == 'DELETE':
        for photo_object in PHOTOS:
            if photo_object.get('id') == photo_object_id:
                PHOTOS.remove(photo_object)
    return jsonify(response_object)


def download_image(url, file_path, file_name):
    full_path = file_path + '/' + file_name + '.jpg'
    urllib.request.urlretrieve(url, full_path)



def create_cav(images_dir):
    images_dir = Path('examples/images')
    my_cav = CAV.load('examples/roundness.cav')

    for image in images_dir.iterdir():
        print(image.name, my_cav.score(image))




# @app.route('/concept', methods=['POST', 'GET'])  # url for my app
# def concept(concept, photos):
#     pass


if __name__ == "__main__":
    app.run(debug=True)