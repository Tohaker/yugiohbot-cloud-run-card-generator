import datetime
import logging
import os
import random
import shutil
import ntpath

import requests
from flask import Flask
from flask import request

from card import neocardmaker as neo
from utils import gcsutils

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)


@app.route('/')
def handler():
    logging.debug(request.args)

    title = request.args.get('title')
    effect = request.args.get('effect')
    card_template = request.args.get('template')
    logging.debug('Received title: ' + title)
    logging.debug('Received effect: ' + effect)
    logging.debug('Received template: ' + card_template)

    storage_client = gcsutils.create_storage_client(False)
    image_destination, card_image_path, is_submission = choose_card_image(storage_client)

    rarity = ['common', 'rare', 'ultra', 'secret']
    # template options are ['Normal', 'Effect', 'Ritual', 'Synchro', 'DarkSynchro', 'Xyz', 'Spell', 'Trap', 'Fusion']
    race = ['Aqua', 'Beast', 'Beast-Warrior', 'Creator-God', 'Cyberse', 'Dinosaur', 'Divine-Beast', 'Dragon',
            'Fairy', 'Fiend', 'Fish', 'Insect', 'Machine', 'Plant', 'Psychic', 'Pyro', 'Reptile', 'Rock', 'Sea Serpent',
            'Spellcaster', 'Thunder', 'Warrior', 'Winged Beast']

    card_rarity = random.choice(rarity)
    card_attribute = create_card_attribute(card_template)
    card_race = random.choice(race)
    card_type = create_card_type(card_template, card_race)
    card_icon = choose_card_icon(card_template)
    card_level = random.randint(0, 12)

    attack, defense = choose_card_stats(card_level)
    card_serial = str(random.randint(0, 9999999999))

    final_image_path = datetime.datetime.now().strftime("%d-%m-%Y-%H:%M:%S") + '.jpg'

    logging.debug('rarity: ' + card_rarity)
    logging.debug('template: ' + card_template)
    logging.debug('attribute: ' + card_attribute)
    logging.debug('type: ' + card_type)
    logging.debug('attack : ' + attack)
    logging.debug('defense: ' + defense)
    logging.debug('serial: ' + card_serial)

    neo.create_card(name=title, rarity=card_rarity, template=card_template, attribute=card_attribute,
                    level=str(card_level), picture=card_image_path, type=card_type, icon=card_icon,
                    effect=effect, atk=attack, defense=defense, creator='YuGiOh-Bot',
                    year=str(datetime.date.today().year),
                    serial=card_serial, filename=final_image_path)

    gcsutils.upload_card(final_image_path, storage_client)

    if is_submission:
        image_destination = 'Submission from a fan - submit yours at https://yugiohbot3000.github.io/submission/....'

    res = requests.post("https://us-east1-yugiohbot.cloudfunctions.net/yugiohbot__card-uploader",
                        json={"title": title, "image": final_image_path, "card_image": image_destination[:-4]})

    logging.debug(res)

    result = {'card_file': final_image_path}
    logging.debug(result)
    return result


def download_from_shitpostbot():
    base = 'https://www.shitpostbot.com/'
    rand_url = 'api/randsource'

    image_url = base + requests.get(base + rand_url).json()['sub']['img']['full']
    file_name = ntpath.basename(image_url)

    response = requests.get(image_url, stream=True)
    file = open(file_name, 'wb')
    response.raw.decode_content = True
    shutil.copyfileobj(response.raw, file)

    return file_name


def choose_card_image(storage_client):
    # 20% chance of getting a shitpostbot source image.
    is_submission = False
    if random.random() < 0.2:
        image_destination = download_from_shitpostbot()
    else:
        prefix = 'cropped'
        if random.random() < 0.3:
            prefix = 'submissions'
            is_submission = True

        image = str(random.choice(gcsutils.list_files_in_bucket('yugiohbot-images', prefix, storage_client)).name)
        logging.debug('Chosen image: ' + image)
        image_destination = image.replace(prefix + '/', '')
        gcsutils.download_image(image, image_destination, storage_client)

    card_image_path = os.path.abspath(image_destination)
    logging.debug('Full path: ' + card_image_path)

    return image_destination, card_image_path, is_submission


def create_card_type(template, race):
    if template == 'Spell' or template == 'Trap':
        card_type = '{} Card'.format(template)
    elif template != 'Normal' and template != 'Effect':
        card_type = race + ' / ' + template + ' / Effect'
    elif template != 'Normal':
        card_type = race + ' / ' + template
    else:
        card_type = race

    return card_type


def create_card_attribute(template):
    attribute = ['None', 'Dark', 'Divine', 'Earth', 'Fire', 'Light', 'Water', 'Wind']
    if template == 'Spell' or template == 'Trap':
        card_attribute = template
    else:
        card_attribute = random.choice(attribute)
    return card_attribute


def choose_card_icon(template):
    spell_type = ['None', 'Continuous', 'Counter', 'Equip', 'Field', 'Quick-play', 'Ritual']
    trap_type = ['None', 'Continuous', 'Counter']

    if template == 'Spell':
        card_icon = random.choice(spell_type)
    elif template == 'Trap':
        card_icon = random.choice(trap_type)
    else:
        card_icon = 'None'

    return card_icon


def choose_card_stats(level):
    max_stats = {
        0: 0,
        1: 500,
        2: 1000,
        3: 1750,
        4: 2000,
        5: 2600,
        6: 2600,
        7: 3000,
        8: 3000,
        9: 4000,
        10: 4000,
        11: 5000,
        12: 5000
    }

    attack = str(int(round(random.randint(0, max_stats.get(level)), -2)))
    defense = str(int(round(random.randint(0, max_stats.get(level)), -2)))

    return attack, defense


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
