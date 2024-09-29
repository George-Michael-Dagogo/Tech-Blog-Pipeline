# %% [markdown]
# ### Import Libraries and Install

# %%
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pandas as pd

# %%
#pip install fake_useragent pandas "pymongo[srv]" nltk langid pycountry

# %% [markdown]
# ## Scraping dev.to

# %%
url = 'https://dev.to/'

ua = UserAgent()
userAgent = ua.random
headers = {'User-Agent': userAgent}
page = requests.get(url, headers = headers)
soup = BeautifulSoup(page.content, "html.parser")
print(url)
blog_box = soup.find_all('div', class_= "crayons-story")

links = []
titles = []
time_uploaded = []
authors = []
tags = []
reading_times = []

for box in blog_box:
    #links
    if box.find('h2', class_ = "crayons-story__title") is not None:
        link = box.find('h2', class_ = "crayons-story__title").a  #.replace('\n\t\t','').replace('\n','').strip()
        link = link['href']
        links.append('https://dev.to'+ link)
    else:
        links.append('None')

    #titles
    if box.find('h2', class_ = "crayons-story__title") is not None:
        title = box.find('h2', class_ = "crayons-story__title").text.replace('\n','').strip()
        titles.append(title)
    else:
        titles.append('None')

    #time_uploaded
    if box.find('time', attrs={"datetime": True}) is not None:
        time_upload = box.find('time', attrs={"datetime": True})   #.replace('\n\t\t','').replace('\n','').strip()
        time_upload = time_upload['datetime']
        time_uploaded.append(time_upload)
    else:
        time_uploaded.append('None') 

    #author
    if box.find('a', class_ ="crayons-story__secondary fw-medium m:hidden") is not None:
        author = box.find('a', class_ ="crayons-story__secondary fw-medium m:hidden").text.replace('\n','').strip()
        authors.append(author)
    else:
        authors.append('None')

    #tags
    if box.find('div', class_ ="crayons-story__tags") is not None:
        tag = box.find('div', class_ ="crayons-story__tags").text.replace('\n','').strip()
        tags.append(tag)
    else:
        tags.append('None')

    #reading_time
    if box.find('div', class_ ="crayons-story__save") is not None:
        reading_time = box.find('div', class_ ="crayons-story__save").text.replace('\n','').strip()
        reading_times.append(reading_time)
    else:
        reading_times.append('None')

df = pd.DataFrame({
    'Link': links,
    'Title': titles,
    'Time Uploaded': time_uploaded,
    'Author': authors,
    'Tags': tags,
    'Reading Time': reading_times
})

df_cleaned = df[df['Link'] != 'None']

article = []
article_link = []
def get_full_content(url): 
    ua = UserAgent()
    userAgent = ua.random
    headers = {'User-Agent': userAgent}
    page = requests.get(url, headers = headers)
    soup = BeautifulSoup(page.content, "html.parser")
    print(url)
    content = soup.find('div', class_= "crayons-article__body text-styles spec__body")
    paragraphs = content.find_all('p')
    contents = []
    # Iterate over each <p> tag and remove any <a> tags within them
    for paragraph in paragraphs:
        for a in paragraph.find_all('a'):
            a.decompose()  # Removes <a> tag and its content

    # Print the cleaned text from each <p> tag
    for paragraph in paragraphs:
        contents.append(paragraph.get_text())

    string = ' '.join(contents)
    article.append(string)
    article_link.append(url)

for i in df_cleaned.Link:
    get_full_content(i)


article_df = pd.DataFrame({
    'Article Content': article,
    'Link': article_link
})


merged_df = pd.merge(df_cleaned, article_df, on='Link', how='inner')
merged_df

# %% [markdown]
# ## Getting the Word Count, Sentiment and Polarity Score of the Article Content

# %%
from nltk.corpus import stopwords
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

df = merged_df
# Download the stopwords dataset
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('vader_lexicon')
nltk.download('punkt_tab')


def count_words_without_stopwords(text):
    if isinstance(text, (str, bytes)):
        words = nltk.word_tokenize(str(text))
        stop_words = set(stopwords.words('english'))
        filtered_words = [word for word in words if word.lower() not in stop_words]
        return len(filtered_words)
    else:
        0

df['Word Count'] = df['Article Content'].apply(count_words_without_stopwords)


sid = SentimentIntensityAnalyzer()

def get_sentiment(row):
    sentiment_scores = sid.polarity_scores(row)
    compound_score = sentiment_scores['compound']

    if compound_score >= 0.05:
        sentiment = 'Positive'
    elif compound_score <= -0.05:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'

    return sentiment, compound_score

df[['Sentiment', 'Compound Score']] = df['Article Content'].astype(str).apply(lambda x: pd.Series(get_sentiment(x)))

df

# %% [markdown]
# ## Detecting the Language of each Article Content

# %%
import pandas as pd
import langid
import pycountry


def detect_language(text):
    # Convert NaN to an empty string
    text = str(text) if pd.notna(text) else ''
    
    # Use langid to detect the language
    lang, confidence = langid.classify(text)
    return lang

df['Language'] = df['Article Content'].apply(detect_language)
df['Language'] = df['Language'].map(lambda code: pycountry.languages.get(alpha_2=code).name if pycountry.languages.get(alpha_2=code) else code)
df



# %% [markdown]
# ## Testing for successful handshake

# %%

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://testtech:Your_password@cluster0.ahrx7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# %% [markdown]
# ## Moving our data to MongoDB Atlas

# %%
uri = "mongodb+srv://testtech:Your_password@cluster0.ahrx7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


# Specify the database and collection
db = client['my_database']  # Create/use 'my_database'
collection = db['article_collection']  # Create/use 'my_collection'

# Convert DataFrame to dictionary (list of dictionaries)
data = df.to_dict(orient='records')

# Insert the data into the MongoDB collection
result = collection.insert_many(data)

# Print the inserted IDs
print("Inserted document IDs:", result.inserted_ids)



# Step 1: Identify duplicates
pipeline = [
    {
        "$group": {
            "_id": "$Link",  # Field to check for duplicates
            "uniqueIds": { "$addToSet": "$_id" },  # Store all unique _ids
            "count": { "$sum": 1 }  # Count duplicates
        }
    },
    {
        "$match": {
            "count": { "$gt": 1 }  # Only keep duplicates
        }
    }
]

duplicates = collection.aggregate(pipeline)

# Step 2: Remove duplicates
for doc in duplicates:
    unique_ids = doc['uniqueIds']
    unique_ids.pop(0)  # Keep the first id
    # Delete the duplicates
    collection.delete_many({"_id": {"$in": unique_ids}})

print("Duplicates removed.")



