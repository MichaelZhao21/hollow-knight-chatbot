# Hollow Knight Chatbot

Simple chatbot that will tell you information from the Hollow Knight Wiki! pls don't roast i dont do this stuff normally TT

## Setup

To install Python libraries, create a virtual environment & activate it then run

```bash
pip install -r requirements.txt
```

## Execution

### Scraping and processing data

To scrape the data, run `python scrape.py`. This will output the raw HTML data into `output-raw`.

To process the scraped data, run `python process.py`. This will output the processed knowledge base into `output-data`.

Note that scraping does take a while (600+ pages!). To skip this step, simply run `extract.sh`. This will extract the `output-raw` and `output-data` from the zipped archives to be used in the next step. On the other hand, if you do manually run the scripts, you can zip all the files simply by running `zip-data.sh`.

### Model Training

TODO: Not done smh