# Artificial Vision: Colorization of Manga

## File organisation

- the ```CUT``` folder contains a clone of the original CUT repository with the files (models) tailored to our needs.
- the ```CycleGAN``` folder contains a clone of the original CycleGAN repository with the files (models) tailored to our needs.
- the ```dataset-builder``` folder contains a script to download the images and another script to scale down the images (see ```DATASET_GENERATION.md``` for more information).
- the ```upsampling.ipynb``` is the notebook we sued to produce our upsampling results using LapSRN and EDSR deep sampling models.
- the ```test_*.sh``` are srcipts to colorize your images (see the section **Running new classifications**).
- the ```metrics.sh``` is a script that produce the three metrics used in the article PSNR, SSIM, channel histogram difference.



### Authors

With equals contributions:
  - Otavio Flores Jacobi
  - Dylan Hertay
  - Théo Matricon
  - Julien Mazué

### Running new classifications

 - We know pushing heavy models to github is not the optimal way of sharing CNN weights. However, due to us not wanting to pay for a better storage system, we use it anyway :). In order to reduce the space consumed by the model, we push only the CUT Generator networks weights, which can be found on folders `CUT/checkpoints/one_piece_256` and `CUT/checkpoints/one_piece_512`.

The first model run 256x256 classifications and the second one works on 512x512 images.

If you have all the modules required in `CUT/requirements.txt` you can test our weights in our sample images `sample/testA/*.jpg` files, and you can add new images there and run files `test_256.sh` or `test_512.sh` to colorize your manga images :) Beware to always use 512x512 B&W original manga as input for optimal results.

Results will be available in the `results` folder. Be aware to always save your results because this folder will be deleted when running the any of the `test_*.sh` files.
