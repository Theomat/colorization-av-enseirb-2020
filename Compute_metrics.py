import sys
from os import walk,path
from PIL import Image
from math import log10, sqrt
from skimage.metrics import structural_similarity as ssim
import numpy as np

def PSNR(img1, img2): 
    mse = np.mean(pow(img1 - img2, 2)) 
    if mse == 0:
        return 100
    max_pixel = 255.0
    psnr = 20 * log10(max_pixel / sqrt(mse)) 
    return psnr 

directory = []
index = 0
for arg in sys.argv:
    if index != 0:
        directory.append(arg)
    index += 1
if index != 3:
    raise Exception("2 files needed")

listfile = [[],[]]
for i in range(2):
    for (repertoire, sousRepertoires, fichiers) in walk(directory[i]):
        listfile[i].extend(fichiers)
        break

image = []
ssim_value = []
psnr_value = []

for i in range(len(listfile[0])):
    for j in range(len(listfile[1])):
        if '.'.join(listfile[0][i].split('.')[:-1]) == '.'.join(listfile[1][j].split('.')[:-1]):
            img1 = np.array(Image.open(path.join(directory[0],listfile[0][i])))
            img2 = np.array(Image.open(path.join(directory[1],listfile[1][j])))
            image.append(listfile[1][j])
            ssim_value.append(ssim(img1,img2,multichannel=True))
            psnr_value.append(PSNR(img1,img2))
            break

#print(image)
#print(ssim_value)
#print(psnr_value)
print("\n Metrics :\n")
print("SSIM_MIN :",np.min(ssim_value)," Image :",image[np.argmin(ssim_value)])
print("SSIM_Mean :",np.mean(ssim_value))
print("SSIM_Mediane :",np.median(ssim_value))
print("SSIM_MAX :",np.max(ssim_value)," Image :",image[np.argmax(ssim_value)])
print(" ")
print("PSNR_MIN :",np.min(psnr_value)," Image :",image[np.argmin(psnr_value)])
print("PSNR_Mean :",np.mean(psnr_value))
print("PSNR_Mediane :",np.median(psnr_value))
print("PSNR_MAX :",np.max(psnr_value)," Image :",image[np.argmax(psnr_value)])
