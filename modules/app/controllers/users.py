''' controller and routes for users '''
import os
import pandas as pd
from flask import request, jsonify, render_template
from app import app, listings
import logger
import matplotlib.pyplot as plt

import re
from wordcloud import WordCloud, STOPWORDS
from .constants import STOPWORDS

ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(
    __name__, filename=os.path.join(ROOT_PATH, 'output.log'))



@app.route('/data')
def user():
    all_listing_in_country = listings.aggregate([{
        "$group": {
            "_id": "$address.country",
            "mean_price": {
                "$avg": "$price"
            }
        }
    }])
    plt.tight_layout()

    df = pd.DataFrame(list(all_listing_in_country))
    df.mean_price = df.mean_price.astype('str').astype('float')

    ax = df.plot.bar(x='_id')
    ax.set_xlabel("Country")
    ax.figure.savefig('./app/static/pricePlot.png',bbox_inches='tight')
    keys = []
    vals = []
    for c in all_listing_in_country:
        keys.append(c["_id"])
        vals.append(c["mean_price"])
    res = dict(zip(keys, vals))

    summary = listings.find({"amenities": {"$all": ["Internet"]}})

    summary = list(summary)
    df = pd.DataFrame(summary)
    text = df['summary'].tolist()
    text_string = ' '.join(text)
    freqMap = getFrequencyDictForText(text_string)

    create_word_cloud(freqMap)
    return jsonify(freqMap), 200


def create_word_cloud(string):
    cloud = WordCloud(background_color="black", max_words=1000)
    cloud.generate_from_frequencies(string)
    cloud.to_file("./app/static/wordCloud.png")



def getFrequencyDictForText(sentence):
    tmpDict = {}

    # making dict for counting frequencies
    for curr in sentence.split(" "):
        if not curr in STOPWORDS and re.match("^[a-zA-Z]*$", curr):
            val = tmpDict.get(curr, 0)
            tmpDict[curr.lower()] = val + 1

    return tmpDict
