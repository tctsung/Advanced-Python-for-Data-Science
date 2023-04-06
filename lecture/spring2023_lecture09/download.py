import os
import requests
from pathlib import Path
from time import time

types = {'image/jpeg', 'image/png', 'image/gif'}

def get_links(client_id):
    '''used to obtain a list of available images'''
    headers = {'Authorization': 'Client-ID {}'.format(client_id)}
    r = requests.get('https://api.imgur.com/3/gallery/random/random/', headers=headers)

    data = r.json()
    return [item['link'] for item in data['data'] if 'type' in item and item['type'] in types]

def download_link(directory, link):
    '''downloads the image given by the URL _link_ into _directory_'''
    download_path = directory / os.path.basename(link)
    with download_path.open('wb') as f:
        f.write(requests.get(link).content)

def setup_download_dir():
    '''creates a download destination directory if it doesn’t already exist'''
    download_dir = Path('images')
    if not download_dir.exists():
        download_dir.mkdir()
    return download_dir





## other examples in the lecture

import numpy as np

def sum_multi_processes_1(chunk):
    y = 0
    for i in chunk:
        y = y + i
    return y

def sum_multi_processes_2(start, end):
    y = 0
    for i in range(start, end):
        y = y + i
    return y

def monte_carlo_pi(n):
    s = 0
    for i in range(n):
        x = np.random.uniform(0, 1)
        y = np.random.uniform(0, 1)
        if (x**2 + y**2) < 1:
            s += 1
    return 4*s/n
