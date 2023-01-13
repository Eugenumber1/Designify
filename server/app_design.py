import uuid
from flask import Flask, url_for, request, redirect, jsonify
from flask import render_template
from pyunsplash import PyUnsplash
from flask_cors import CORS


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
    {
        'id': uuid.uuid4().hex,
        'word': 'Tadj Mahal',
        'url': ['https://unsplash.com/photos/S34fEzWT6eE/download?ixid=MnwzOTEwNTZ8MXwxfHNlYXJjaHwxfHxpbm5vdmF0aW9ufGVufDB8fHx8MTY3MzUyNjg5Mg']
    },
    {
        'id': uuid.uuid4().hex,
        'word': 'Something Else',
        'url': ['https://unsplash.com/photos/G7VN8NadjO0/download?ixid=MnwzOTEwNTZ8MHwxfHNlYXJjaHw3fHxpbm5vdmF0aW9ufGVufDB8fHx8MTY3MzUyNjg5Mg']
    }
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
        search = py_un.search(type_='photos', per_page=50, query=word)
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
        photo_object['url'] = photos
        response_object['photos'] = photo_object
        PHOTOS.append(photo_object)
        response_object['message'] = 'Photo added!'
        print(response_object)
        return jsonify(response_object)
    else:
        response_object['photos'] = PHOTOS
        return jsonify(response_object)



# @app.route('/concept', methods=['POST', 'GET'])  # url for my app
# def concept(concept, photos):
#     pass


if __name__ == "__main__":
    app.run(debug=True)