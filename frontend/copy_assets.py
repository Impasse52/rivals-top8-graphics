import shutil
from distutils.dir_util import copy_tree

copy_tree("../backend/static/Resources", "./build/static/Resources")

shutil.rmtree("../backend/static/build")
shutil.move("./build", "../backend/static/build")
