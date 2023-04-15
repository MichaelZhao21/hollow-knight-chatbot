import spacy
from Levenshtein import distance
import nltk
import numpy as np
import string
import urllib.parse
import re
import tensorflow as tf
import os
import json


def read_kb():
    pattern = re.compile('[\W_]+', re.UNICODE)

    # Read knowledge base
    kb = dict()
    topics = list()

    for filename in os.listdir('output-kb'):
        with open('output-kb/' + filename, 'r') as file:
            key = pattern.sub('', urllib.parse.unquote(
                filename.replace('_(Hollow_Knight)', ''))).lower()
            kb[key] = json.load(file)
            topics.append(key)

    return kb, topics


def load_intents():
    """Load the intents from the intents.json file"""
    with open("intents.json") as file:
        data = json.load(file)
    return data


def parse_intents(intents: dict, lemmatizer):
    """Parse the intents to get the words, classes, X and y"""

    # Create empty lists
    words = []
    classes = []

    for intent in intents:
        for pattern in intent['patterns']:
            tokens = nltk.word_tokenize(pattern)
            words.extend(tokens)

        if intent['intent'] not in classes:
            classes.append(intent['intent'])

    # Lemmatize words and convert to lowercase
    words = [lemmatizer.lemmatize(word.lower())
             for word in words if word not in string.punctuation]

    # sort words and classes alphabetically
    # to make sure no duplicates
    words = sorted(set(words))
    classes = sorted(set(classes))

    return words, classes


def load_model():
    """Load the model from the model.h5 file"""
    model = tf.keras.models.load_model("chatbot_model.h5")
    return model


def min_dist(word: str, vec: list[str]):
    min = 2**32 - 1
    min_word = ""
    for v in vec:
        d = distance(word, v)
        if d < min:
            min = d
            min_word = v
    return min_word, min


def get_topic(message: str, topics: list[str], nlp: spacy.Language):
    # Lowercase message string and replace non alphanumeric characters
    message = re.sub(r'[^a-zA-Z0-9\s]', '', message.lower())

    doc = nlp(message)
    min = 2**32 - 1
    min_text = ""
    for chunk in doc.noun_chunks:
        curr_text, curr_val = min_dist(chunk.text.lower(), topics)
        if curr_val < min:
            min = curr_val
            min_text = curr_text
    return min_text


def clean_text(text, lemmatizer):
    tokens = nltk.word_tokenize(text)
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return tokens


def bag_of_words(text, vocab, lemmatizer):
    tokens = clean_text(text, lemmatizer)
    bow = [0] * len(vocab)
    for w in tokens:
        for idx, word in enumerate(vocab):
            if word == w:
                bow[idx] = 1
    return np.array(bow)


def pred_class(text, vocab, labels, model, lemmatizer):
    bow = bag_of_words(text, vocab, lemmatizer)
    result = model.predict(np.array([bow]), verbose='none')[0]
    thresh = 0.2
    y_pred = [[idx, res] for idx, res in enumerate(result) if res > thresh]

    y_pred.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in y_pred:
        return_list.append(labels[r[0]])
    return return_list


def get_response_from_dict(topic, intent, kb):
    # Check for basic intents
    if intent == "greeting":
        return "Hi there, how can I help?"
    if intent == "farewell":
        return "See you later, have a nice day!"
    if intent == "thanks":
        return "You're welcome!"
    if intent == "help":
        return "I can help you with Hollow Knight related information! Type a query to ask a question."

    # Return a response from the knowledge base
    if intent not in kb[topic]:
        return "I'm sorry, I don't understand."
    return kb[topic][intent]


def get_response(query, topics, words, classes, nlp, kb, model, lemmatizer):
    res_intents = pred_class(query, words, classes, model, lemmatizer)
    if len(res_intents) == 0:
        return "I'm sorry, I don't understand."

    topic = get_topic(query, topics, nlp)

    # Debug statements
    # print("Topic: ", topic)
    # print("Intent: ", res_intents[0])

    return get_response_from_dict(topic, res_intents[0], kb)


def main():
    # Load knowledge base
    kb, topics = read_kb()

    # Load intents
    intents = load_intents()

    # Load model
    model = load_model()

    # Load spacy
    nlp = spacy.load("en_core_web_sm")

    # Load lemmatizer
    lemmatizer = nltk.stem.WordNetLemmatizer()

    # Parse intents
    words, classes = parse_intents(intents, lemmatizer)

    print("\nBot is ready to talk. Type 'quit' to exit\n")
    while True:
        query = input("You: ")
        print()
        if query == "quit":
            break
        print("<Bot> ", get_response(query, topics,
              words, classes, nlp, kb, model, lemmatizer))
        print()


if __name__ == "__main__":
    main()
