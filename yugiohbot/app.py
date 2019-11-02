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
    flavour = request.args.get('flavour')
    logging.debug('Received title: ' + title)
    logging.debug('Received effect: ' + effect)
    logging.debug('Received flavour: ' + flavour)

    card_image = str(random.choice(gcsutils.list_files_in_bucket('yugiohbot-images')).name)
    logging.debug('Chosen image: ' + card_image)
    image_destination = card_image.replace('cropped/', '')
    gcsutils.download_image(card_image, image_destination)
    card_image_path = os.path.abspath(image_destination)
    logging.debug('Full path: ' + card_image_path)

    rarity = ['common', 'rare', 'ultra', 'secret']
    template = ['Normal', 'Effect', 'Ritual', 'Synchro', 'DarkSynchro', 'Xyz']
    attribute = ['None', 'Dark', 'Divine', 'Earth', 'Fire', 'Light', 'Water', 'Wind']
    race = ['Aqua', 'Beast', 'Beast-Warrior', 'Creator-God', 'Cyberse', 'Dinosaur', 'Divine-Beast', 'Dragon',
            'Fairy', 'Fiend', 'Fish', 'Insect', 'Machine', 'Plant', 'Psychic', 'Pyro', 'Reptile', 'Rock', 'Sea Serpent',
            'Spellcaster', 'Thunder', 'Warrior', 'Winged Beast']

    card_rarity = random.choice(rarity)
    card_template = random.choice(template)
    card_attribute = random.choice(attribute)
    card_race = random.choice(race)

    if card_template != 'Normal' and card_template != 'Effect':
        card_type = card_race + '/ ' + card_template + '/ Effect'
    elif card_template != 'Effect':
        card_type = card_race + '/ ' + card_template
    else:
        card_type = card_race

    if card_template == 'Normal':
        text = flavour
    else:
        text = effect

    attack = str(int(round(random.randint(0, 7000), -2)))
    defense = str(int(round(random.randint(0, 7000), -2)))
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
                    level=str(random.randint(0, 12)), picture=card_image_path, type=card_type,
                    effect=text, atk=attack, defense=defense, creator='YuGiOh-Bot',
                    year=str(datetime.date.today().year),
                    serial=card_serial, filename=final_image_path)

    gcsutils.upload_card(final_image_path)

    res = requests.post("https://us-east1-yugiohbot.cloudfunctions.net/yugiohbot__card-uploader",
                        json={"title": title, "image": final_image_path})

    logging.debug(res)

    result = {'card_file': final_image_path}
    logging.debug(result)
    return result


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
