import argparse
import sys
import os
from typing import Dict, List, Callable, Tuple
from io import BytesIO
import re

import tqdm
from PIL import Image
import requests
import js2py

# python3 dataset-builder/crawler.py --src bato --start-img 2 "1496178" "1527640"

# =============================================================================
# Sources specifics
# =============================================================================

# -----------------------------------------------------------------------------
# read
# -----------------------------------------------------------------------------
READ_PATTERN = re.compile(r"\<img src=\"(?P<url>[^\"]*)\"(\s|\n)* class=\"m.-3 mx-auto js-page\"")
READ_BASE_URL = "https://ww{0}.com/chapter/{name}-chapter-{chapter}/"


def read_get_url(name: str, chapter: int, alternative: bool = False):
    url_complement: List[str] = name[:name.index(":")]
    name: str = name[name.index(":") + 1:]
    if alternative:
        chapter: str = "{}".format(chapter)
    else:
        chapter: str = "{:3d}".format(chapter)
    return READ_BASE_URL.format(url_complement, name=name, chapter=str(chapter).zfill(3))


def read_get_links(name: str, chapter: int, r) -> List[str]:
    text = r.text
    urls = []
    for match in re.finditer(READ_PATTERN, text):
        url = match.groupdict()["url"]
        if url[-1] == "\r":
            url = url[:-1]
        urls.append(url)
    return urls


# -----------------------------------------------------------------------------
# bato
# -----------------------------------------------------------------------------
BATO_LINK_DEF = re.compile(r"const images = \[([^\]]*)\];")
BATO_LINK = re.compile(r"\"(?P<url>[^\"]*)\"")
BATO_BATO = re.compile(r"const batojs = ([^;]*);")
BATO_SERVER = re.compile(r"const server = \"([^;]*)\";")


def bato_get_url(name: str, chapter: int, **kwargs) -> str:
    return f"https://bato.to/chapter/{int(name) + chapter - 1}"


def bato_get_links(name: str, chapter: int, r) -> List[str]:
    text = r.text
    line: str = re.findall(BATO_LINK_DEF, text)[0]
    urls: List[str] = []
    for match in re.finditer(BATO_LINK, line):
        url: str = match.groupdict()["url"]
        urls.append(url)

    batojs = js2py.eval_js(re.findall(BATO_BATO, text)[0])
    JSON = js2py.eval_js('JSON')
    CryptoJS = js2py.require("crypto-js", True)
    server: str = re.findall(BATO_SERVER, text)[0]
    result: str = JSON.parse(CryptoJS.AES.decrypt(server, batojs).toString(CryptoJS.enc.Utf8))
    return [result + url for url in urls]


# -----------------------------------------------------------------------------
SPECIFICS: Dict[str, Dict[str, Callable]] = {
    "read": {
        "url": read_get_url,
        "links": read_get_links
    },
    "bato": {
        "url": bato_get_url,
        "links": bato_get_links
    }
}
# =============================================================================
# Argument parsing
# =============================================================================
parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Crawler to download images from a manga.")
parser.add_argument('name_bw', type=str, help="url name of the manga in BW")
parser.add_argument('name_colored', type=str, help="url name of the manga in color")
parser.add_argument('-o', '--output', help="output folder", default=None)
parser.add_argument('--min', dest='chapter_min', default=1, type=int)
parser.add_argument('--max', dest='chapter_max', default=1, type=int)
parser.add_argument('--trim-end', dest='trim_end', action='store_const', const=True, default=False,
                    help="when different size trim at the end insetad of the start")
parser.add_argument('-v', '--verbose', dest='verbose', action='store_const', const=True, default=False)
parser.add_argument('--shift', dest='shift', default=0, type=int, help="relative shift of images number")
parser.add_argument('--start-img', dest='start_img', default=1, type=int, help="starting image from 1")


# =============================================================================
# General use function
# =============================================================================
def download_image(url: str, path: str) -> bool:
    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        image = Image.open(BytesIO(r.content))
        image.save(path)
        return True
    return False


# =============================================================================
# =============================================================================
# =============================================================================
def get_chapter_images(name: str, chapter: int, verbose: bool = False) -> Tuple[bool, List[str]]:
    source: str = list(SPECIFICS.keys())[0]
    if ":" in name:
        source: str = name[:name.index(":")]
        name: str = name[name.index(":") + 1:]
    url: str = SPECIFICS[source]["url"](name, chapter)
    if verbose:
        print("[checking] url=", url)
    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        return True, SPECIFICS[source]["links"](name, chapter, r)
    else:
        other_url: str = SPECIFICS[source]["url"](name, chapter, True)
        if other_url != url:
            r = requests.get(other_url)
            if r.status_code == requests.codes.ok:
                return True, SPECIFICS[source]["links"](name, chapter, r)
        print(f"[checking] failed: {r.status_code}")
        return False, []


def download_images(bw_images_urls: List[str], color_image_urls: List[str], c_path: str, bw_path: str) -> int:
    index: int = 0
    images: int = 0
    for i in tqdm.trange(len(bw_urls), desc="images"):
        bw, color = bw_urls[i], colored_urls[i]

        path_bw: str = f"{bw_path}_{index}.png"
        path_colored: str = f"{c_path}_{index}.png"
        if download_image(bw, path_bw) and download_image(color, path_colored):
            images += 1
        else:
            # Delete if failed
            if os.path.exists(path_bw):
                os.remove(path_bw)
        index += 1
    return images


# =============================================================================
# Main
# =============================================================================
parameters = parser.parse_args(sys.argv[1:])
parameters.output = parameters.output or parameters.name_bw.replace("-", "_")
total_chapters_success: int = 0
total_images: int = 0
folder: str = os.path.join("./dataset/", parameters.output)
for chapter in tqdm.trange(parameters.chapter_min, parameters.chapter_max + 1, desc="chapter"):
    success, bw_urls = get_chapter_images(parameters.name_bw, chapter, parameters.verbose)
    if not success:
        continue
    success, colored_urls = get_chapter_images(parameters.name_colored, chapter, parameters.verbose)
    if not success:
        continue
    # Create folder
    bw_folder: str = os.path.join(folder, "bw")
    colored_folder: str = os.path.join(folder, "colored")
    if not os.path.exists(folder):
        if not os.path.exists("./dataset"):
            os.mkdir("./dataset")
        os.mkdir(folder)
    if not os.path.exists(bw_folder):
        os.mkdir(bw_folder)
    if not os.path.exists(colored_folder):
        os.mkdir(colored_folder)

    if parameters.shift > 0:
        bw_urls: List[str] = bw_urls[parameters.shift:]
    elif parameters.shift < 0:
        colored_urls: List[str] = colored_urls[-parameters.shift:]
    # Trim according to start images
    if len(bw_urls) != len(colored_urls):
        mini: int = min(len(bw_urls), len(colored_urls))
        if parameters.trim_end:
            bw_urls: List[str] = bw_urls[:mini]
            colored_urls: List[str] = colored_urls[:mini]
        else:
            bw_urls: List[str] = bw_urls[-mini:]
            colored_urls: List[str] = colored_urls[-mini:]
    start_index: int = parameters.start_img - 1
    bw_urls: List[str] = bw_urls[start_index:]
    colored_urls: List[str] = colored_urls[start_index:]
    # Download the images
    images: int = download_images(bw_urls, colored_urls, os.path.join(folder, 'colored', f"chapter_{chapter}"), os.path.join(folder, 'bw', f"chapter_{chapter}"))
    total_images += images
print(f"Saved a total of {total_images} images !")
