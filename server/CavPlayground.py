from pathlib import Path
import cavlib

pngs = Path('/Users/zhenyabudnyk/Documents/myProjects/mood-board-search/backend/static-cav-content/jpgs')
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



