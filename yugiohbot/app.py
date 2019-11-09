import datetime
import logging
import os
import random

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

    card_image = str(random.choice(gcsutils.list_files_in_bucket('yugiohbot-images')).name)
    logging.debug('Chosen image: ' + card_image)
    image_destination = card_image.replace('cropped/', '')
    gcsutils.download_image(card_image, image_destination)
    card_image_path = os.path.abspath(image_destination)
    logging.debug('Full path: ' + card_image_path)

    rarity = ['common', 'rare', 'ultra', 'secret']
    # template options are ['Normal', 'Effect', 'Ritual', 'Synchro', 'DarkSynchro', 'Xyz', 'Spell', 'Trap', 'Fusion']
    attribute = ['None', 'Dark', 'Divine', 'Earth', 'Fire', 'Light', 'Water', 'Wind']
    race = ['Aqua', 'Beast', 'Beast-Warrior', 'Creator-God', 'Cyberse', 'Dinosaur', 'Divine-Beast', 'Dragon',
            'Fairy', 'Fiend', 'Fish', 'Insect', 'Machine', 'Plant', 'Psychic', 'Pyro', 'Reptile', 'Rock', 'Sea Serpent',
            'Spellcaster', 'Thunder', 'Warrior', 'Winged Beast']
    spell_type = ['None', 'Continuous', 'Counter', 'Equip', 'Field', 'Quick-play', 'Ritual']
    trap_type = ['None', 'Continuous', 'Counter']

    card_rarity = random.choice(rarity)
    card_attribute = random.choice(attribute)
    card_race = random.choice(race)

    if card_template != 'Normal' and card_template != 'Effect':
        card_type = card_race + '/ ' + card_template + '/ Effect'
    elif card_template != 'Normal':
        card_type = card_race + '/ ' + card_template
    elif card_template == 'Spell' or card_template == 'Trap':
        card_type = '{} Card'.format(card_template)
        card_attribute = card_template
    else:
        card_type = card_race

    card_icon = 'None'
    if card_template == 'Spell':
        card_icon = random.choice(spell_type)
    elif card_template == 'Trap':
        card_icon = random.choice(trap_type)

    card_level = random.randint(0, 12)

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

    attack = str(int(round(random.randint(0, max_stats.get(card_level)), -2)))
    defense = str(int(round(random.randint(0, max_stats.get(card_level)), -2)))
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

    gcsutils.upload_card(final_image_path)

    res = requests.post("https://us-east1-yugiohbot.cloudfunctions.net/yugiohbot__card-uploader",
                        json={"title": title, "image": final_image_path, "card_image": image_destination[:-4]})

    logging.debug(res)

    result = {'card_file': final_image_path}
    logging.debug(result)
    return result


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
