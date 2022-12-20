from flask import Flask, url_for, request, redirect
from flask import render_template
from pyunsplash import PyUnsplash


from datetime import datetime




# ------------ ATOMIC VARS ---------------


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'you-will-never-guess'
api_key = 'mJpXOSabo4pvepg4JaPEOMhBWUxmS86hQIvueQQezx4'
py_un = PyUnsplash(api_key=api_key)








# --------------- API -------------------

@app.route('/', methods=['POST', 'GET'])  # url for my app
def home():
    if request.method == "POST":
        word = request.form['word-search']
        search = py_un.search(type_='photos', per_page=50, query=word)
        photos = list()
        print(type(search))
        for entry in search.entries:
            photos.append(entry.link_download)
            print(entry.link_download)
        print(len(photos))
        return render_template("concept.html", concept=word, photos=photos)
    return render_template("home.html")


@app.route('/concept', methods=['POST', 'GET'])  # url for my app
def concept(concept, photos):
    pass







if __name__ == "__main__":
    app.run(debug=True)