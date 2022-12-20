import logging
from pyunsplash import PyUnsplash
api_key = 'mJpXOSabo4pvepg4JaPEOMhBWUxmS86hQIvueQQezx4'

# instantiate PyUnsplash object
py_un = PyUnsplash(api_key=api_key)

# pyunsplash logger defaults to level logging.ERROR
# If you need to change that, use getLogger/setLevel
# on the module logger, like this:
#logging.getLogger("pyunsplash").setLevel(logging.DEBUG)


search = py_un.search(type_='photos', query='innovation')
#print(len(search.entries))
for entry in search.entries:
    print(entry.link_html)

# Start with the generic collection, maximize number of items
# note: this will run until all photos of all collections have
#       been visited, unless a connection error occurs.
#       Typically the API hourly limit gets hit during this
#
# collections = py_un.collections(per_page=30)
# while collections.has_next:
#     for collection in collections.entries:
#         photos = collection.photos()
#         for photo in photos.entries:
#             print(collection.title, photo.link_download, photo.get_attribution())

    # no need to specify per_page: will take from original object
    #collections = collections.get_next_page()