import json
import string
import random
import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout

nltk.download("punkt")
nltk.download("wordnet")


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
    X = []
    y = []

    for intent in intents:
        for pattern in intent['patterns']:
            tokens = nltk.word_tokenize(pattern)
            words.extend(tokens)
            X.append(pattern)
            y.append(intent['intent'])

        if intent['intent'] not in classes:
            classes.append(intent['intent'])

    # Lemmatize words and convert to lowercase
    words = [lemmatizer.lemmatize(word.lower())
             for word in words if word not in string.punctuation]

    # sort words and classes alphabetically
    # to make sure no duplicates
    words = sorted(set(words))
    classes = sorted(set(classes))

    return words, classes, X, y


def create_training_data(words, classes, X, y, lemmatizer):
    """Create the training data for the model by converting the words to a bag of words model"""
    training = []
    out_empty = [0] * len(classes)

    # BAG OF WORDS Model
    for ind, s in enumerate(X):
        bow = []
        text = lemmatizer.lemmatize(s.lower())
        for word in words:
            bow.append(1) if word in text else bow.append(0)

        output_row = list(out_empty)
        output_row[classes.index(y[ind])] = 1

        training.append([bow, output_row])

    # Shuffle the data
    random.shuffle(training)
    training = np.array(training, dtype=object)

    # split the features and target labels
    train_X = np.array(list(training[:, 0]))
    train_y = np.array(list(training[:, 1]))

    return train_X, train_y


def create_model(train_X, train_y):
    """Create the model: 2 hidden layers with 128 neurons each and 1 output layer with 3 neurons"""
    input_shape = (len(train_X[0]),)
    output_shape = len(train_y[0])
    epochs = 400

    model = Sequential()
    model.add(Dense(128, input_shape=input_shape, activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(128, input_shape=input_shape, activation="relu"))
    model.add(Dropout(0.3))
    model.add(Dense(output_shape, activation="softmax"))

    adam = tf.keras.optimizers.Adam(learning_rate=0.1)
    model.compile(loss='categorical_crossentropy',
                  optimizer=adam,
                  metrics=["accuracy"])
    print(model.summary())
    model.fit(x=train_X, y=train_y, epochs=epochs, verbose=1)

    return model


def main():
    # Get the lemmatizer
    lemmatizer = WordNetLemmatizer()

    # Load the intents
    intents = load_intents()

    # Parse the intents
    words, classes, X, y = parse_intents(intents, lemmatizer)

    # Create the training data
    train_X, train_y = create_training_data(words, classes, X, y, lemmatizer)

    # Create the model
    model = create_model(train_X, train_y)

    # Save the model
    model.save("chatbot_model.h5", save_format="h5")


if __name__ == "__main__":
    main()
