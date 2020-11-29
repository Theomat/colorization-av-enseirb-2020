import os

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, datasets

import natsort
from PIL import Image

import numpy as np

import random

import torchvision.models as models

from skimage import color

class MangaDataset(Dataset):
    def __init__(self, main_dir, transform=None):
        
        self.bw_dir = os.path.join(main_dir, 'bw')
        self.color_dir = os.path.join(main_dir, 'colored')
        
        
        self.transform = transform
        
        colored_imgs = os.listdir(self.color_dir)
        bw_imgs = os.listdir(self.bw_dir)
        
        self.total_colored_imgs = natsort.natsorted(colored_imgs)
        self.total_bw_imgs = natsort.natsorted(bw_imgs)
        
        assert len(self.total_colored_imgs) == len(self.total_bw_imgs)

    def __len__(self):
        return len(self.total_colored_imgs)

    def __getitem__(self, idx):
        
        target_img = os.path.join(self.color_dir, self.total_colored_imgs[idx])
        out_np = np.asarray(Image.open(target_img).resize((256,256), resample=3))
        
        img_lab_orig = color.rgb2lab(out_np)
        
        ipt = img_lab_orig[:, :, 0]
        out = img_lab_orig[:, :, 1:]
        
        out = np.stack((out[:, :, 0], out[:, :, 1]))
        
        # [256, 256, 2] -> [2, 256, 256]
        tensor_input = torch.Tensor(ipt).unsqueeze(0)
        tensor_target = torch.Tensor(out)
                
        return tensor_input, tensor_target