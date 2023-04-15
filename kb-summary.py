import re
import urllib.parse
import os
import json


def read_kb():
    """Read the knowledge base from the output-kb folder"""
    # Read knowledge base
    kb = dict()

    for filename in os.listdir('output-kb'):
        with open('output-kb/' + filename, 'r') as file:
            kb[filename] = json.load(file)

    return kb


def main():
    with open('kb-summary.txt', 'w') as file:
        kb = read_kb()
        for topic in kb:
            file.write(topic + ':\n')
            for intent in kb[topic]:
                file.write(f'\t{intent}: ')
                file.write(' '.join(kb[topic][intent].split(' ')[:10]) + '...\n')


if __name__ == '__main__':
    main()
