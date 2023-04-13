from transformers import pipeline
import json
import sys
import os
from pathlib import Path

INTENTS_TO_REMOVE = ['greeting', 'farewell', 'thank you', 'help']


def read_intents() -> dict:
    with open('intents.json', 'r') as file:
        intents = json.load(file)
        labels = [a['intent'] for a in intents]
        for i in INTENTS_TO_REMOVE:
            labels.remove(i)
        return labels


def classify(classifier, labels, text: str):
    """Classify the text and return the label and the text"""
    prediction = classifier(text, labels, multi_label=True)
    print(f'\t [{prediction["labels"][0]}] is label for "{" ".join(prediction["sequence"].split(" ")[:4])}..." with confidence {prediction["scores"][0]}')
    return (prediction['labels'][0], prediction['sequence'])


def process_file(classifier, intents, file):
    """Process the files and write to a new document"""
    print(f'Processing file {file.name.replace("output-data/", "")}...')
    # Read all lines and split into sentences
    lines = '\n'.join(file.readlines())
    sequence_lists = [s.strip() for s in lines.split('.') if s.strip() != ""]

    # Classify each sentence
    out_list = []
    for sequence in sequence_lists:
        if len(sequence.split(' ')) > 3:
            out_list.append(classify(classifier, intents, sequence))

    # Take each intent and combine all sentences into one string
    kb = dict()
    for entry in out_list:
        if entry[0] in kb:
            kb[entry[0]] += entry[1] + '. '
        else:
            kb[entry[0]] = entry[1] + '. '

    # Write the knowledge base to a file
    with open(file.name.replace('output-data', 'output-kb'), 'w') as outfile:
        json.dump(kb, outfile, indent=4)

    print(f'Finished processing {file.name}')


def main():
    # Create output dir
    Path("output-kb").mkdir(parents=True, exist_ok=True)

    # Load classifier model
    print('Loading classifier model...')
    classifier = pipeline('zero-shot-classification',
                          model='facebook/bart-large-mnli')
    print('Classifier model loaded!')

    # Read intents file
    intents = read_intents()

    # Check if there is a command line argument to continue the parsing
    cont_parse = ""
    if len(sys.argv) > 1:
        cont_parse = ' '.join(sys.argv[1:])

    # Get all files
    files = os.listdir('output-data')

    # If the command line argument exists, find the location in the list
    split_index = 0
    if cont_parse != "":
        split_index = files.index(cont_parse)
        if split_index < 0:
            print(f'Invalid name: {cont_parse}')
            return

    # Split the list
    if split_index > 0:
        files = files[split_index:]

    # Iterate through the files and process all files
    for filename in files:
        with open('output-data/' + filename, 'r') as file:
            process_file(classifier, intents, file)


if __name__ == '__main__':
    main()

##### PAUSED AT: Exploration_(Hollow_Knight) #####
##### 2:03:53 #####
##### Progress: 123/657 = 18.7% #####