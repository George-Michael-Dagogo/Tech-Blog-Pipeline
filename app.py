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

load_dotenv()

# MongoDB connection details
uri = os.environ['URI_KEY']
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['my_database'] 
collection = db['article_collection'] 

# Load MongoDB data
data = pd.DataFrame(list(collection.find()))
# Streamlit title and description
st.title("Interactive Article Insights Dashboard")
st.write("Explore and interact with article data from MongoDB.")

# Convert 'Reading Time' to numeric by extracting the number from the string
data['Reading Time'] = data['Reading Time'].str.extract('(\d+)').astype(float)
data['Time Uploaded'] = pd.to_datetime(data['Time Uploaded'], utc=True)


# Sidebar filters
st.sidebar.title("Filters")

# Filter by Author
author = st.sidebar.selectbox('Select Author', options=['All'] + list(data['Author'].unique()))
if author != 'All':
    data = data[data['Author'] == author]

# Filter by Sentiment
sentiment = st.sidebar.multiselect('Select Sentiment', options=data['Sentiment'].unique(), default=data['Sentiment'].unique())
if sentiment:
    data = data[data['Sentiment'].isin(sentiment)]

# Filter by Tags
all_tags = set(tag for tags in data['Tags'].str.split('#') for tag in tags if tag)
tags = st.sidebar.multiselect('Select Tags', options=list(all_tags))
if tags:
    data = data[data['Tags'].apply(lambda x: any(tag in x for tag in tags))]
# Get earliest and latest dates from the dataset
earliest_date = data['Time Uploaded'].min().date()
latest_date = data['Time Uploaded'].max().date()

# Filter by Date Range with restricted date selection
min_date, max_date = st.sidebar.date_input(
    "Select Date Range",
    [earliest_date, latest_date],
    min_value=earliest_date, 
    max_value=latest_date
)

# Convert user input dates to timezone-aware UTC timestamps
min_date = pd.to_datetime(min_date).tz_localize('UTC')
max_date = pd.to_datetime(max_date).tz_localize('UTC')


# Apply Date Filter
data = data[(data['Time Uploaded'] >= min_date) & (data['Time Uploaded'] <= max_date)]
# Apply Date Filter
data = data[(data['Time Uploaded'] >= min_date) & (data['Time Uploaded'] <= max_date)]

# Filter by Word Count and Reading Time
min_word_count, max_word_count = st.sidebar.slider("Word Count Range", min_value=int(data['Word Count'].min()), max_value=int(data['Word Count'].max()), value=(int(data['Word Count'].min()), int(data['Word Count'].max())))
min_reading_time, max_reading_time = st.sidebar.slider("Reading Time Range (minutes)", min_value=0, max_value=int(data['Reading Time'].max()), value=(0, int(data['Reading Time'].max())))

# Apply Word Count and Reading Time Filters
data = data[(data['Word Count'] >= min_word_count) & (data['Word Count'] <= max_word_count)]
data = data[(data['Reading Time'] >= min_reading_time) & (data['Reading Time'] <= max_reading_time)]

# Display summary of filtered data
st.subheader(f"Showing {len(data)} Articles")
st.write(data[['Title', 'Author', 'Time Uploaded', 'Tags', 'Sentiment']])

# Sentiment Distribution
st.subheader("Sentiment Distribution")
fig, ax = plt.subplots()

# Custom palette for sentiment
custom_palette = {
    'Positive': 'green',  # Green for Positive sentiment
    'Neutral': 'grey',         # Grey for Neutral sentiment
    'Negative': 'red'          # Red for Negative sentiment
}

# Use the custom palette in the countplot
sns.countplot(data=data, x='Sentiment', ax=ax, palette=custom_palette, dodge=False)

st.pyplot(fig)




# Reading Time Distribution
st.subheader("Reading Time Distribution")
fig, ax = plt.subplots()
sns.histplot(data['Reading Time'], bins=10, ax=ax, kde=True)
st.pyplot(fig)

# Most Common Tags Visualization
st.subheader("Most Common Tags")
tags_list = data['Tags'].str.split('#').explode()
top_tags = tags_list.value_counts().head(10)
st.bar_chart(top_tags)

# Word Count vs Sentiment with palette and explicit hue
st.subheader("Word Count by Sentiment")
fig, ax = plt.subplots()
sns.boxplot(x='Sentiment', y='Word Count', data=data, ax=ax, hue='Sentiment', palette='Set2', dodge=False, legend=False)
st.pyplot(fig)


# Generate word cloud for Tags
st.subheader("Word Cloud of Tags")
tags_string = ' '.join(tags_list.dropna().values)
wordcloud = WordCloud(background_color='white', width=800, height=400).generate(tags_string)
fig, ax = plt.subplots()
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis('off')
st.pyplot(fig)

# Extract the hour from the 'Time Uploaded' column
data['Upload Hour'] = data['Time Uploaded'].dt.hour

# Visualization for posting times throughout the day
st.subheader("Content Upload Distribution by Hour of the Day")
fig, ax = plt.subplots()

# Create a count plot for upload hours
sns.countplot(data=data, x='Upload Hour', ax=ax, palette='viridis', order=range(24))

ax.set_xticks(range(24))
ax.set_xticklabels([f'{hour}:00' for hour in range(24)], rotation=45)
ax.set_xlabel("Hour of the Day")
ax.set_ylabel("Number of Articles")
ax.set_title("Number of Articles Posted by Hour")

st.pyplot(fig)



# Generate word cloud for Tags
st.write("## Word Cloud for Top Words in Articles")
stop_words = set(stopwords.words('english'))

# Concatenate all the article content into a single string
text = ' '.join(data['Article Content'].dropna())

# Generate the word cloud without stopwords
wordcloud = WordCloud(stopwords=stop_words, background_color='white', width=800, height=400).generate(text)

st.subheader("Word Cloud of Article Content (Without Stopwords)")
fig, ax = plt.subplots(figsize=(10, 5))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis('off')

# Show the plot using Streamlit
st.pyplot(fig)


# Display additional statistics about filtered data
st.subheader("Additional Statistics")
st.write("**Average Word Count**:", data['Word Count'].mean())
st.write("**Average Reading Time**:", data['Reading Time'].mean())
st.write("**Total Articles**:", len(data))
