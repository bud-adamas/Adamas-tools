#!/usr/bin/env python

import os
import shutil
import re
from PIL import Image

# where the original images reside
root_path = '..' + os.sep + 'images'

# where to keep the largest images
keep_path = '..' + os.sep + 'keep'

# two level, a cupboard contains a lot drawers,
# with each drawers containing files with the same prefix
cupboard = {}

print("__name__ is {0}".format(__name__))

if __name__ == '__main__':

  print("root_path is {0}, keep_path is {1}".format(root_path, keep_path))
  # put all the files into the cupboard
  for root, dirs, files in os.walk(root_path):
    print("root is " + root)
    print("files is " + str(files))
    print("\n")

    for file in [x for x in files if x[-4:] == ".jpg"]:
      # all files in JPG format
      file_prefix = re.match('(.*?)( \(\d+\))?.jpg', file).groups()[0]
      if file_prefix in cupboard:
        cupboard[file_prefix].append(root + os.sep + file)
      else:
        cupboard[file_prefix] = [ root + os.sep + file]
  
  # keep the largest file in drawer, and remove others
  for drawer in cupboard:
    print("drawer is " + str(drawer))
    file_to_keep = ""
    width_to_keep = 0
    height_to_keep = 0

    cupboard[drawer].sort()
    for file in cupboard[drawer]:
      im = Image.open(file)
      width, height = im.size
      print("file {0}, width {1}, height {2}".format(file, width, height))
      if file_to_keep == "":
        file_to_keep = file
      else:
        if width > width_to_keep and height > height_to_keep:
          file_to_keep = file
          width_to_keep = width
          height_to_keep = height

    # then move the file to keep to somewhere
    shutil.copy(file_to_keep, keep_path)
