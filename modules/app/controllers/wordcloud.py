import numpy as np
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import matplotlib.pyplot as plt

def wordcloud():
  df = pd.read_csv("data/winemag-data-130k-v2.csv", index_col=0)

