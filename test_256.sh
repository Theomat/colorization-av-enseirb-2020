#!/bin/bash

cd CUT
python test.py --name one_piece_256 --CUT_mode CUT --dataroot ../sample 
cd ..
rm -rf results
mv CUT/results/one_piece_256/test_latest/images/fake_B results
rm -rf CUT/results