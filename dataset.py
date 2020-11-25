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


class MangaDataset(Dataset):
    def __init__(self, main_dir, transform):
        
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
        
        seed = np.random.randint(2147483647) # make a seed with numpy generator 
                
        target_img = os.path.join(self.color_dir, self.total_colored_imgs[idx])
        input_img = os.path.join(self.bw_dir, self.total_bw_imgs[idx])

        target = Image.open(target_img).convert("RGB").resize((1024,1024))

        random.seed(seed) # apply this seed to img tranfsorms
        torch.manual_seed(seed) # needed for torchvision 0.7
        tensor_target = self.transform(target)


        # ATTENTION: we can either use target_img or input_img
        # target_img will generate BW input from colored image
        # input_img will use actual original manga data
        ipt = Image.open(target_img).convert("L").resize((1024,1024))
        
        random.seed(seed) # apply this seed to target tranfsorms
        torch.manual_seed(seed) # needed for torchvision 0.7
        tensor_input = self.transform(ipt)
        
                
        return tensor_input, tensor_target

data_transform = transforms.Compose([
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        #transforms.Normalize(mean=[0.485, 0.456, 0.406],
        #                     std=[0.229, 0.224, 0.225])
])

manga_dataset = MangaDataset('./dataset/one_piece', transform=data_transform)

dataset_loader = torch.utils.data.DataLoader(manga_dataset,
                                             batch_size=4, shuffle=True,
                                             num_workers=4)
