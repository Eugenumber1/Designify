from pathlib import Path
from cavlib import CAV

images_dir = Path('examples/images')
my_cav = CAV.load('examples/roundness.cav')

for image in images_dir.iterdir():
    print(image.name, my_cav.score(image))