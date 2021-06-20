import os
import glob
from PIL import Image
import numpy as np
import random

image_dir = "[DIRECTORY OF SCRAPED IMAGES]"
out_dir = "./out_pruned_images"
os.makedirs(out_dir, exist_ok=True)
filelist = glob.glob(os.path.join(image_dir, "*.png"))
random.shuffle(filelist)

uninteresting_count = 0
uninteresting_sat_stdevs = []
for i, image_path in enumerate(filelist):
    pil_img = Image.open(image_path)
    img = np.array(pil_img)
    H, W, C = img.shape
    sat_img = img[:, :W // 2, :]
    map_img = img[:, W // 2:, :]
    
    map_img_stdev = np.std(map_img.reshape((H * W // 2, C)), axis=0).mean()
    
    if map_img_stdev < 1.0:
        uninteresting_count += 1
        sat_img_stdev = np.std(sat_img.reshape((H * W // 2, C)), axis=0).mean()
        uninteresting_sat_stdevs.append(sat_img_stdev)
        if sat_img_stdev < 30.0:
            out_path = os.path.join(out_dir, os.path.basename(image_path))
            pil_img.save(out_path)
            print(out_path, i / len(filelist) * 100.0)