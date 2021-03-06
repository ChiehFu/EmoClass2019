# -*- coding: utf-8 -*-
"""gen_preprocessed.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1g4HH-heJmDwVDxO8Dip3-uHIWsujgYzB
"""

import argparse
import os
import numpy as np
from PIL import Image
import functional as F

parser = argparse.ArgumentParser()

# Preprocessing
parser.add_argument('--upscale', type=bool, default=False, help='Preprocess: whether to quadruple input pixels')

parser.add_argument('--blur', type=bool, default=False, help='Preprocess: whether to blur inputs')
parser.add_argument('--gs-blur', type=bool, default=False, help='Preprocess: whether to gaussian blur inputs')
parser.add_argument('--sharpen', type=bool, default=False, help='Preprocess: whether to sharpen inputs')

parser.add_argument('--hist-equal', type=bool, default=False, help='Preprocess: whether to do histogram equalization')
parser.add_argument('--gamma-correct', type=bool, default=False, help='Preprocess: whether to do gamma correction')
parser.add_argument('--gamma', type=float, default=0.5, help='Preprocess: gamma value for correction')

parser.add_argument('--landmark', type=bool, default=False, help='Preprocess: whether to add facial landmarks')
parser.add_argument('--angle-correct', type=bool, default=False, help='Preprocess: whether to do face angle correction')

args = parser.parse_args()

if args.upscale:
  data_dir = './dataset_x4_raw'
  gen_dir = './dataset_x4'
else:
  data_dir = './dataset_raw'
  gen_dir = './dataset'

if not os.path.isdir(gen_dir):
  os.mkdir(gen_dir)

for f in os.listdir(data_dir):
  if f == '.DS_Store':
    continue

  gen_folder_dir = os.path.join(gen_dir, f)
  if not os.path.isdir(gen_folder_dir):
    os.mkdir(gen_folder_dir)

  folder_dir = os.path.join(data_dir, f)
  for subf in os.listdir(folder_dir):
    if subf == '.DS_Store':
      continue

    gen_subfolder_dir = os.path.join(gen_folder_dir, subf)
    if not os.path.isdir(gen_subfolder_dir):
      os.mkdir(gen_subfolder_dir)

    subfolder_dir = os.path.join(folder_dir, subf)
    for i in os.listdir(subfolder_dir):
      if i == '.DS_Store':
        continue

      img_dir = os.path.join(subfolder_dir, i)
      img = Image.open(img_dir)

      ## Preprocessing
      if args.blur:
        img = F.blur(img)

      if args.gs_blur == True:
        img = F.gaussian_blur(img)

      if args.sharpen == True:
        img = F.sharpen(img)

      if args.hist_equal == True:
        img = F.histogram_equalize(img)

      if args.gamma_correct == True:
        # gamma < 1: lighter
        # gamma > 1: darker
        img = F.adjust_gamma(img, args.gamma)

      # should be applied on upscaled images
      if args.landmark == True:
        img = F.get_facial_landmark(img)

      if args.angle_correct == True:
        img = F.rotate_by_eyes_angle(img)

      gen_img_dir = os.path.join(gen_subfolder_dir, i)
      img.save(gen_img_dir)
