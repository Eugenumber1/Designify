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
BOOKS = [
    {
        'id': uuid.uuid4().hex,
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'read': True
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J. K. Rowling',
        'read': False
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'read': True
    }
]

# --------------- API -------------------

@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book added!'
    else:
        response_object['books'] = BOOKS
    return jsonify(response_object)

@app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
def single_book(book_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_book(book_id)
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book updated!'
    if request.method == 'DELETE':
        remove_book(book_id)
        response_object['message'] = 'Book removed!'
    return jsonify(response_object)

def remove_book(book_id):
    for book in BOOKS:
        if book['id'] == book_id:
            BOOKS.remove(book)
            return True
    return False

# @app.route('/', methods=['GET'])
# def home():
#     return jsonify('Hello World!')

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('Damn I did it')

@app.route('/', methods=['POST', 'GET'])  # url for my app
def home():
    response_object = {'status': 'success'}
    if request.method == "POST":
        post_data = request.get_json()
        word = post_data.get('word')
        search = py_un.search(type_='photos', per_page=50, query=word)
        photos = list()
        print(type(search))
        for entry in search.entries:
            photos.append(entry.link_download)
            print(entry.link_download)
        print(len(photos))
        response_object['photos'] = photos
        return jsonify(response_object)
    return jsonify(response_object)


# @app.route('/concept', methods=['POST', 'GET'])  # url for my app
# def concept(concept, photos):
#     pass


if __name__ == "__main__":
    app.run(debug=True)