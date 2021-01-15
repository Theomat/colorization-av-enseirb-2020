from PIL import Image
import os, sys
from tqdm import tqdm

path = "./dataset/one_piece/bw/"
dirs = os.listdir( path )

print(dirs)

for item in tqdm(dirs):
    if os.path.isfile(path+item):
        im = Image.open(path+item).convert("RGB")
        f, e = os.path.splitext(path+item)
        imResize = im.resize((512, 512), Image.ANTIALIAS)
        os.remove(path+item)
        imResize.save(f + '.jpg', 'JPEG', quality=90)
