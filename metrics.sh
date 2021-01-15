#!/bin/bash


for i in {5..400..5}
do
    python test.py --name one_piece_cut_reduced --CUT_mode CUT --dataroot ./datasets/sample --phase train --epoch "${i}" --load_size 512 --crop_size 512
done

rm -rf results/psnr
mkdir results/psnr

for i in {5..400..5}
do
    cp -r results/one_piece_cut_reduced/train_"${i}"/images/fake_B results/psnr/fake_B_"${i}"
done

python psnr.py