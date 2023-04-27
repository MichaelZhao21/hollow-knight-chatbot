# Hollow Knight Chatbot

Simple chatbot that will tell you information from the Hollow Knight Wiki! pls don't roast i dont do this stuff normally TT

## Data Preperation

### Setup

To install Python libraries, create a virtual environment & activate it then run

```bash
pip install -r requirements.txt
```

You may also need to install a spacy module:

```bash
python3 -m spacy download en_core_web_sm
```

### Scraping and processing data

> NOTE: You can skip this section and simply run `extract.sh`

1. To scrape the data, run `python scrape.py`. This will output the raw HTML data into `output-raw`.
2. To process the scraped data, run `python process.py`. This will output scraped text from the HTML into `output-data`.
3. To form the knowledge base, run `python knowledge.py`. This will use a classification model to form a knowledge base and output into `output-kb`.

Note that scraping does take a while (600+ pages, ~10 mins on relatively bad wifi). Forming the knowledge base also takes a hella long time (LIKE ALMOST 11 HOURS). `extract.sh` will help as the zips will be uploaded to the repo.

To skip this step, simply run `extract.sh`. This will extract the `output-raw`, `output-data`, and `output-kb` directories from the zipped archives to be used in the next step. On the other hand, if you do manually run the scripts, you can zip all the files simply by running `zip-data.sh`.

### Model Training

We will create our own model to classify the questions into specific intents. To train the model on the intents, run `python train.py`. This is surprisingly fast (which probably means it is bad).

## Running the Bot

### DOCKER

The app has been dockerized!!! Once you have the `output-kb` folder and everything installed, you can simply run `docker compose up` and the app should run.

### Setup

The bot is a combination of Rasa and custom actions that connect with my underlying knowledge base.

To set up the bot, you will need [Conda](https://docs.conda.io/en/latest/). After doing so, you should [create the environment from the environment.yml file](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file). The environment will be named `rasa`. Don't forget to activate it after!

```bash
conda env create -f environment.yml
conda activate rasa
```

You will need to train the chatbot using the following command. This should take <5 minutes and output the model in the `models` directory:

```bash
rasa train
```

Since the bot uses a custom action responder, you will need to run the actions server separately:

```bash
rasa run actions
```

Once that is running, open a new terminal and run the bot

```bash
rasa shell --endpoints endpoints-local.yml
```
