#!/bin/bash

for i in {5..200..5}
do
    #cp checkpoints/one_piece_cycle/"${i}"_net_G_A.pth checkpoints/one_piece_cycle/"${i}"_net_G.pth 
    python test.py --name one_piece_cycle --dataroot ./datasets/sample --phase train --epoch "${i}" --no_dropout --model cycle_gan
done

mkdir results/psnr


for i in {5..200..5}
do
    rm -rf results/psnr/fake_B_"${i}"
    mkdir results/psnr/fake_B_"${i}"
    cp results/one_piece_cycle/train_"${i}"/images/*_fake_B.png results/psnr/fake_B_"${i}/"
done

python psnr.py