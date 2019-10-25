import shutil
import urllib.parse
import logging

import requests


# We can generate a card image using the following API:
# https://www.yugiohcardmaker.net/ycmaker/createcard.php?name=&cardtype=Monster&subtype=normal&attribute=Light&level=1
# &rarity=Common&picture=&circulation=&set1=&set2=&type=&carddescription=&atk=&def=&creator=&year=2019&serial=

# https://www.yugiohcardmaker.net/ycmaker/createcard.php?name=&cardtype=Spell&trapmagictype=Quick-Play&rarity=Common
# &picture=&circulation=&set1=&set2=&carddescription=&creator=&year=2019&serial=

def construct_request(**kwargs):
    base_url = "https://www.yugiohcardmaker.net/ycmaker/createcard.php?"
    url_args = ['name', 'cardtype', 'trapmagictype', 'subtype', 'attribute', 'level', 'rarity', 'picture',
                'circulation', 'set1', 'set2', 'type', 'carddescription', 'atk', 'def', 'creator', 'year', 'serial']
    url_dict = {}

    for arg in url_args:
        # index = url_args.index(arg)
        kw = kwargs.get(arg) if kwargs.get(arg) is not None else ""  # Check if the Key Word argument has been supplied.
        url_dict[arg] = kw  # Build up a dictionary of all the arguments.

    base_url += urllib.parse.urlencode(url_dict)
    return base_url


def download_image(url, path):
    try:
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(path, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
    except Exception as e:
        logging.debug('Error downloading image: ' + str(e))
