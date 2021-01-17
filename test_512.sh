#!/bin/bash

cd CUT
python test.py --name one_piece_512 --CUT_mode CUT --dataroot ../sample --load_size 512 --crop_size 512
cd ..
rm -rf results
mv CUT/results/one_piece_512/test_latest/images/fake_B results
rm -rf CUT/results