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

EPOCHS = 10
BATCH_SIZE = 8

trainDataset = MangaDataset('../colorization-av-enseirb-2020/dataset/one_piece', train=True)

trainLoader = torch.utils.data.DataLoader(trainDataset,
                                             batch_size=BATCH_SIZE, shuffle=True,
                                             num_workers=4)

testDataset = MangaDataset('../colorization-av-enseirb-2020/dataset/one_piece', train=False)

testLoader = torch.utils.data.DataLoader(testDataset,
                                             batch_size=BATCH_SIZE, shuffle=True,
                                             num_workers=4)


colorizer_eccv16 = eccv16(pretrained=True).eval().to(device)

writer = SummaryWriter()

criterion = nn.MSELoss()
optimizer = torch.optim.Adam(colorizer_eccv16.parameters(), lr=3.16e-5, betas=(0.9, 0.99), eps=1e-08, weight_decay=0.001)


print('Training using' + device)

for epoch in range(EPOCHS):
    total_running_loss = 0.0
    total = 0
    for i, batch in enumerate(trainLoader, 0):

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
        total += 1
        
    with torch.no_grad():
        colorizer_eccv16.eval()
        total_test_loss = 0.0
        total_test = 0
        for i_tst, batch_test in enumerate(testLoader, 0):
            ipt_tst, target_tst = batch_test
            ipt_tst, target_tst = ipt_tst.to(device), target_tst.to(device)

            y_pred = colorizer_eccv16(ipt_tst)
            total_test_loss += criterion(target_tst, y_pred).item()
            total_test += 1

        colorizer_eccv16.train()

    print("avg running", total_running_loss/float(total))
    print("avg test", total_test_loss/float(total_test))

    writer.add_scalar('train_loss', total_running_loss/float(total), epoch)
    writer.add_scalar('test_loss', total_test_loss/float(total_test), epoch)
torch.save(colorizer_eccv16.state_dict(), 'model.pt')