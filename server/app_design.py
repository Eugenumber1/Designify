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
import boto3
import random



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
s3 = boto3.client('s3', aws_access_key_id='AKIA4TY6Y5CRV7VPBSMD',
                  aws_secret_access_key='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', region_name='eu-central-1',
                  config=boto3.session.Config(signature_version='s3v4',))

# ------------RESOURCES------------

CONCEPTS = [
    # {
    #     'id': uuid.uuid4().hex,
    #     'word': 'Tadj Mahal',
    #     'url': ['https://unsplash.com/photos/S34fEzWT6eE/download?ixid=MnwzOTEwNTZ8MXwxfHNlYXJjaHwxfHxpbm5vdmF0aW9ufGVufDB8fHx8MTY3MzUyNjg5Mg']
    # },
    # {
    #     'id': uuid.uuid4().hex,
    #     'word': 'Something Else',
    #     'url_positive': ['https://unsplash.com/photos/G7VN8NadjO0/download?ixid=MnwzOTEwNTZ8MHwxfHNlYXJjaHw3fHxpbm5vdmF0aW9ufGVufDB8fHx8MTY3MzUyNjg5Mg']
    #     'url_negative': ['kjwfnkafnlksjnfksndfgk']
    # }
]


# --------------- API -------------------


@app.route('/photos', methods=['POST', 'GET'])  # url for my app
def home():
    s3_photos = s3.list_objects_v2(Bucket="brief-project-for-cm", Prefix="jpgs/")
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
        concept = dict()
        concept['id'] = uuid.uuid4().hex
        concept['word'] = word
        #print(photo_object['word'])
        concept['url_positive'] = dict()
        concept['url_negative'] = dict()
        parameter = 3
        for photo_positive in photos:
            concept['url_positive'][uuid.uuid4().hex] = [photo_positive, parameter]
        random.shuffle(s3_photos['Contents'])
        for obj in s3_photos['Contents'][:31]:
            photo_negative = s3.generate_presigned_url(
                ClientMethod="get_object",
                Params={"Bucket": "brief-project-for-cm", "Key": obj["Key"]}
            )
            concept['url_negative'][uuid.uuid4().hex] = [photo_negative, parameter]
        print(len(concept['url_negative']))
        response_object['concepts'] = concept
        CONCEPTS.append(concept)
        response_object['message'] = 'Photo added!'
        print(response_object)
        return jsonify(response_object)
    else:
        response_object['concepts'] = CONCEPTS
        return jsonify(response_object)

@app.route('/photos/<concept_id>/<photo_id>', methods=['PUT', 'DELETE'])
def single_photo(concept_id, photo_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        put_data = request.get_json()
        if update_photo(concept_id, photo_id, put_data.get('weight')):
            response_object['message'] = 'Weight was updated!'
    if request.method == 'DELETE':
        if remove_photo(concept_id, photo_id):
            response_object['message'] = 'Photo was deleted'
    return jsonify(response_object)


# update photo
def update_photo(concept_id, photo_id, weight):
    for concept in CONCEPTS:
        if concept['id'] == concept_id:
            if photo_id in concept['url_positive']:
                concept['url_positive'][photo_id][1] = int(weight)
                return True
            elif photo_id in concept['url_negative']:
                concept['url_negative'][photo_id][1] = int(weight)
                return True
    return False

# remove photo
def remove_photo(concept_id, photo_id):
    for concept in CONCEPTS:
        if concept['id'] == concept_id:
            if photo_id in concept['url_positive']:
                concept['url_positive'].pop(photo_id)
                return True
            elif photo_id in concept['url_negative']:
                concept['url_negative'].pop(photo_id)
    return False

@app.route('/concept/<concept_id>', methods=['POST', 'DELETE'])
def concept(concept_id):
    response_object = {'status': 'success'}
    if request.method == 'POST':
        for concept in CONCEPTS:
            if concept.get('id') == concept_id:
                parent = '/Users/zhenyabudnyk/PycharmProjects/Designify/unsplash_pics'
                directory = concept_id
                path = os.path.join(parent, directory)
                print(path)
                os.makedirs(path, exist_ok=True)
                print(path)
                for (key, value) in tqdm(concept.get('url_positive').items()):
                     download_image(value[0], path, key)
                CONCEPTS.remove(concept)
    if request.method == 'DELETE':
        for concept in CONCEPTS:
            if concept.get('id') == concept_id:
                CONCEPTS.remove(concept)
    return jsonify(response_object)


def download_image(url, file_path, file_name):
    full_path = file_path + '/' + file_name + '.jpg'
    urllib.request.urlretrieve(url, full_path)



def create_cav(images_dir):
    images_dir = Path('examples/images')
    my_cav = CAV.load('examples/roundness.cav')

    for image in images_dir.iterdir():
        print(image.name, my_cav.score(image))

@app.route('/designer/<concept_id>', methods=['GET', 'POST', 'DELETE'])
def designerSide(concept_id):
    pass







# @app.route('/concept', methods=['POST', 'GET'])  # url for my app
# def concept(concept, photos):
#     pass


if __name__ == "__main__":
    app.run(debug=True)