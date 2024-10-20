import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd
from nltk.corpus import stopwords
import nltk
from dotenv import load_dotenv
import os
import nltk
nltk.download('stopwords')

load_dotenv()

# MongoDB connection details
uri = os.environ['URI_KEY']
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['my_database'] 
collection = db['article_collection'] 

# Load MongoDB data
data = pd.DataFrame(list(collection.find()))