from pathlib import Path
import cavlib
from PIL import Image, UnidentifiedImageError
import numpy as np
import cv2 as cv
import os

# positives = concept.get('positives')
# negatives = concept.get('negatives')
# concept_cav = cavlib.train_cav(positive_images=positives, negative_images=negatives, model_layer='googlenet_5b')
old_cav = cavlib.CAV.load('/Users/zhenyabudnyk/PycharmProjects/Designify/CAVs/cav1.cav')

pngs = Path('/Users/zhenyabudnyk/Documents/myProjects/mood-board-search/backend/static-cav-content/jpgs')
jpgs = Path('/Users/zhenyabudnyk/PycharmProjects/flickr_scraper/images/abstract')
image_files = list(jpgs.iterdir())
image_files2 = list()
# for image in image_files:
for i, image in enumerate(image_files):
    try:
        pil_image = Image.open(image)
    except UnidentifiedImageError:
        os.remove(str(image))
        print("deleted" + str(i))

jpgs = Path('/Users/zhenyabudnyk/PycharmProjects/flickr_scraper/images/abstract')
image_files = list(jpgs.iterdir())



for image in image_files:
    pass
    # print(image)

    # try:
    #     img = cv.imread(str(image))
    #     if img is None:
    #         continue
    #     img = cv.resize(img, (224, 224), 3)
    #     # img = Image.open(image)
    #     img = np.array(img)
    #     image_files2.append(img)
    # except PIL.UnidentifiedImageError:
    #     continue

sorted_images = old_cav.sort(image_files, reverse=True)
# data = list()
# for i, photo in enumerate(sorted_images[:101]):
#     im = PIL.Image.fromarray(photo)
#     data.append(im.save('sorted_images'+str(i)+'.png'))


print('top 3 images:', sorted_images)
image_files = list(pngs.iterdir())
# images_dir = Path('/Users/zhenyabudnyk/PycharmProjects/Designify/unsplash_pics/2689eb44a5654dfb8efef42612267d6b')
# imgs_p = list()
# imgs_neg = Path('/Users/zhenyabudnyk/PycharmProjects/Designify/unsplash_pics/5d38f3df5e644fd8b0b6a63d8ad9e9a7')
# neg = list()
#
# for image in images_dir.iterdir():
#     imgs_p.append(image)
#
# for image in imgs_neg.iterdir():
#     neg.append(image)
#
# new_cav = cavlib.train_cav(positive_images=imgs_p, negative_images=neg, model_layer='googlenet_5b')
# new_cav.save('/Users/zhenyabudnyk/PycharmProjects/Designify/CAVs/cav1.cav')

# old_cav = cavlib.CAV.load('/Users/zhenyabudnyk/PycharmProjects/Designify/CAVs/cav1.cav')
#
# sorted_images = old_cav.sort(image_files, reverse=True)
# print('top 3 images:', sorted_images[0:3])

image = "https://unsplash.com/photos/ZN5lN-H2kMw/download?ixid=MnwxMjA3fDF8MXxzZWFyY2h8MXx8c3BvcnR8ZW58MHx8fHwxNjc1OTU1NjU0&force=true"


t_im = cavlib.TrainingImage(image=image, weight=5)
print(t_im)



