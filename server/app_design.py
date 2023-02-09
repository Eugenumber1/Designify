import uuid

import cavlib
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

MOODBOARDS = [

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
                Params={"Bucket": "brief-project-for-cm", "Key": obj["Key"]})
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
                path_positive = os.path.join(path, 'positives')
                path_negative = os.path.join(path, 'negatives')
                os.makedirs(path_positive, exist_ok=True)
                os.makedirs(path_negative, exist_ok=True)
                for (key, value) in tqdm(concept.get('url_positive').items()):
                     download_image(value[0], path_positive, key)
                for (key, value) in tqdm(concept.get('url_negative').items()):
                     download_image(value[0], path_negative, key)
                CONCEPTS.remove(concept)
                create_moodboard(concept_id)
    if request.method == 'DELETE':
        for concept in CONCEPTS:
            if concept.get('id') == concept_id:
                CONCEPTS.remove(concept)
    return jsonify(response_object)


def download_image(url, file_path, file_name):
    full_path = file_path + '/' + file_name + '.jpg'
    urllib.request.urlretrieve(url, full_path)

@app.route('/designer/moodboard', methods=['GET'])
def designerSide():
    response_object = {'status': 'success'}
    if request.method == 'GET':
        response_object['moodboards'] = MOODBOARDS
    return jsonify(response_object)

def create_moodboard(concept_id):
    sorted_images = create_cav(concept_id)
    print('top 3 images:', sorted_images[0:3])
    moodboard = dict()
    moodboard['id'] = concept_id
    moodboard['urls'] = dict()
    for image in sorted_images[0:101]:
        # image = str(image) if isinstance(image, Path) else image
        # with open(image, 'rb') as data:
        s3.upload_file(str(image), 'brief-project-for-cm', 'designer-view/'+str(image))
        moodboard['urls'][uuid.uuid4().hex] = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': 'brief-project-for-cm',
                'Key': 'designer-view/' + str(image)
            },)
    MOODBOARDS.append(moodboard)

def create_cav(concept_id):
    concept_positives = Path('/Users/zhenyabudnyk/PycharmProjects/Designify/unsplash_pics/' + concept_id + '/positives')
    concept_negatives = Path('/Users/zhenyabudnyk/PycharmProjects/Designify/unsplash_pics/' + concept_id + '/negatives')
    positives = list(concept_positives.iterdir())
    negatives = list(concept_negatives.iterdir())
    concept_cav = cavlib.train_cav(positive_images=positives, negative_images=negatives, model_layer='googlenet_4d')
    jpgs = Path('/Users/zhenyabudnyk/Documents/myProjects/mood-board-search/backend/static-cav-content/jpgs')
    image_files = list(jpgs.iterdir())
    sorted_images = concept_cav.sort(image_files, reverse=True)
    return sorted_images







# @app.route('/concept', methods=['POST', 'GET'])  # url for my app
# def concept(concept, photos):
#     pass


if __name__ == "__main__":
    app.run(debug=True)