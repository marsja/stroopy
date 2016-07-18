import codecs
import csv
import os
import re

def parse_instructions(input, START, END):

        m = re.compile(r'%s(.*)%s' % (START, END), re.DOTALL | re.MULTILINE)
        text = m.search(input).group(1)

        return text


def read_instructions_file(instructionsfile, START, END):

    with codecs.open(instructionsfile, 'r', encoding='utf-8') as instructions:
        input_data = instructions.read()
        text = parse_instructions(input_data, START, END)

    return text

def create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def write_csv(fileName, thisTrial):

    full_path = os.path.abspath(fileName)
    directory = os.path.dirname(full_path)
    create_dir(directory)

    if not os.path.isfile(full_path):
        with codecs.open(full_path, 'ab+', encoding='utf8') as f:
            csv.writer(f, delimiter=';').writerow(thisTrial.keys())
            csv.writer(f, delimiter=';').writerow(thisTrial.values())
    else:
        with codecs.open(full_path, 'ab+', encoding='utf8') as f:
            csv.writer(f, delimiter=';').writerow(thisTrial.values())
