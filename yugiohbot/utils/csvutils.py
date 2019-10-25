import csv
import logging


def get_card_ids(file):
    card_ids = []

    try:
        with open(file, encoding="utf8") as csvfile:
            read_csv = csv.reader(csvfile)
            for row in read_csv:
                if read_csv.line_num != 1:
                    card_ids.append(row[0])
    except FileNotFoundError as fe:
        logging.debug('File: ' + file + ' could not be found.\n' + str(fe))

    return card_ids
