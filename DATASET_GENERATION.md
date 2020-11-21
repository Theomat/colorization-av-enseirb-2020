# Dataset Generation

It can be done easily with the script ```dataset-builder/imagedl.py```.

To see the usage help:

```
python dataset-builder/imagedl.py _h
```

## Sources supported

- ```bato```: https://bato.to/chapter/1262257
- ```readsnk```: https://ww7.readsnk.com/chapter/shingeki-no-kyojin-chapter-001/

## Dependencies

To install the python dependencies :
```
pip install -r ""./dataset-builder/requirements.txt"
```
And then you need ```npm``` for ```bato```.

## Examples


- **One Piece**:
  - Chapter 1 (51 images): ```python dataset-builder/imagedl.py --start-img 2 -o "one_piece" "bato:1451139" "bato:774999"```
  - Chapter 1-931 (47 481 images):```python dataset-builder/imagedl.py --shift -2 -o "one_piece" --min 1 --max 931 "read:8.readonepiece:one-piece" "read:8.readonepiece:one-piece-digital-colored-comics"```
- **Hunter x Hunter**:
  - Chapter 1-69  (1 242 images):```python dataset-builder/imagedl.py -o "hunter_x_hunter" --min 1 --max 69 "read:2.readhxh:hunter-x-hunter" "read:2.readhxh:hunter-x-hunter-colored"```
  - Chapter 339-360  (396 images):```python dataset-builder/imagedl.py -o "hunter_x_hunter" --min 339 --max 360 "read:2.readhxh:hunter-x-hunter" "read:2.readhxh:hunter-x-hunter-colored"```

- **My Hero Academia**:
  - Chapter 234-290 with holes so actually 34 chapters (476 images): ```python dataset-builder/imagedl.py -o "my_hero_academia" --min 234 --max 290 "read:6.readmha:boku-no-hero-academia" "read:6.readmha:boku-no-hero-academia-colored"```

- **Naruto**:
  - Chapter 1-41 (2 142 images): ```python dataset-builder/imagedl.py -o "naruto" --min 1 --max 41 --trim-end --start 4 --shift 4 "read:7.readnaruto:naruto" "read:7.readnaruto:naruto-digital-colored-comics"```

- **Bleach**:
  - Chapter 480-601 (2 928 images, although there's an image too many in the middle of black and white colors shifting the offset at image 7): ```python dataset-builder/imagedl.py -o "bleach" --min 480 --max 601 --trim-end --shift 3 "read:3.readbleachmanga:bleach" "read:3.readbleachmanga:bleach-digital-colored-comics"```
- **Attack on titans**:
  - Chapter 1 (51 images): ```python dataset-builder/imagedl.py --start-img 2 -o "attack_on_titans" "read:7.readsnk:shingeki-no-kyojin" "read:7.readsnk:shingeki-no-kyojin-colored"```
