# Hollow Knight Chatbot

Simple chatbot that will tell you information from the Hollow Knight Wiki! pls don't roast i dont do this stuff normally TT

## Setup

To install Python libraries, create a virtual environment & activate it then run

```bash
pip install -r requirements.txt
```

## Execution

### Scraping and processing data

1. To scrape the data, run `python scrape.py`. This will output the raw HTML data into `output-raw`.
2. To process the scraped data, run `python process.py`. This will output scraped text from the HTML into `output-data`.
3. To form the knowledge base, run `python knowledge.py`. This will use a classification model to form a knowledge base and output into `output-kb`.

Note that scraping does take a while (600+ pages, ~10 mins on relatively bad wifi). To skip this step, simply run `extract.sh`. This will extract the `output-raw` and `output-data` from the zipped archives to be used in the next step. On the other hand, if you do manually run the scripts, you can zip all the files simply by running `zip-data.sh`.

Forming the knowledge base also takes a hella long time (LIKE ALMOST 11 HOURS). `extract.sh` will help as the zips will be uploaded to the repo.

### Model Training

We will create our own model to classify the questions into specific intents. To train the model on the intents, run `python train.py`. This is surprisingly fast (which probably means it is bad).

