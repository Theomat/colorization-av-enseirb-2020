from model import eccv16
from dataset import MangaDataset

import torch
import torch.nn as nn

import torch.optim as optim

from skimage import color
from PIL import Image
import numpy as np

from torch.utils.tensorboard import SummaryWriter

device = "cuda:0" if torch.cuda.is_available() else "cpu"

mangaDataset = MangaDataset('../colorization-av-enseirb-2020/dataset/one_piece')

datasetLoader = torch.utils.data.DataLoader(mangaDataset,
                                             batch_size=8, shuffle=True,
                                             num_workers=4)

colorizer_eccv16 = eccv16(pretrained=True).eval().to(device)

writer = SummaryWriter()

EPOCHS = 30

criterion = nn.MSELoss()
optimizer = torch.optim.Adam(colorizer_eccv16.parameters(), lr=3.16e-5, betas=(0.9, 0.99), eps=1e-08, weight_decay=0.001)

for epoch in range(EPOCHS):
    total_running_loss = 0.0
    for i, batch in enumerate(datasetLoader, 0):

        ipt, target = batch
        
        ipt, target = ipt.to(device), target.to(device)
                
        optimizer.zero_grad()

        # forward + backward + optimize
        outputs = colorizer_eccv16(ipt)

        loss = criterion(target, outputs)
        loss.backward()
        optimizer.step()
        
        # print statistics
        total_running_loss += loss.item()
        #if i % 10 == 1:    # print every 2000 mini-batches
        #    print('[%d, %5d] loss: %.3f' %
        #          (epoch + 1, i + 1, running_loss / 10.))
        #    running_loss = 0.0
    print("Avg", total_running_loss)
    writer.add_scalar('train_loss', total_running_loss, epoch)

torch.save(colorizer_eccv16.state_dict(), 'model.pt')