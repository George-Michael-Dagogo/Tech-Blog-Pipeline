# Tech Blog Pipeline: Automated Data Pipeline for Article Insights

## Introduction
This project is an end-to-end automated data pipeline designed for beginners in data engineering. It uses **Python** for web scraping, **MongoDB Atlas** for data storage, and **Streamlit** for data visualization link here - https://tech-blog-pipeline.streamlit.app/. The pipeline is cloud-based and utilizes **GitHub Actions** for automation, allowing you to continuously scrape and visualize blog data in real-time.

## Features
- **Automated Web Scraping**: Scrapes articles from websites (e.g., Dev.to) using Python and BeautifulSoup.
- **MongoDB Atlas Storage**: Stores the scraped data in a scalable NoSQL cloud database.
- **Data Processing**: Performs sentiment analysis, word counts, and language detection using **NLTK** and `langid`.
- **Interactive Dashboard**: Built with **Streamlit**, offering a user-friendly interface for visualizing the article insights. 
- **GitHub Actions Automation**: The data pipeline runs on a daily schedule, ensuring the data is always up to date.

## Key Technologies
- **Python**: For scraping, data processing, and sentiment analysis.
- **MongoDB Atlas**: Cloud-based NoSQL database for data storage.
- **Streamlit**: Framework for building interactive dashboards.
- **GitHub Actions**: Automates the execution of the pipeline.

## How It Works
1. **Web Scraping**: Articles are scraped using Python, extracting titles, authors, tags, reading times, and content.
2. **Data Storage**: The scraped data is stored in MongoDB Atlas as a NoSQL database.
3. **Data Analysis**: NLP techniques like sentiment analysis and language detection are applied.
4. **Visualization**: Insights are presented through an interactive dashboard built with Streamlit.
5. **Automation**: GitHub Actions is used to schedule daily runs of the pipeline or trigger it manually.

## How to Run
1. Clone this repository.
2. Set up MongoDB Atlas and store your `URI_KEY` in a `.env` file.
3. Install the dependencies using:
   ```bash
   pip install -r requirements.txt
4. Run the Streamlit app locally
   ```bash
   streamlit run app.py

## Deployment
The Streamlit app can be deployed on Streamlit Community Cloud by linking this repository. This allows for public access to the dashboard and continuous updates via GitHub Actions.

## Usage
This project is ideal for learning concepts such as:

- Web scraping using Python.
- Working with NoSQL databases (MongoDB).
- Data visualization with Streamlit.
- Automating tasks with GitHub Actions and deploying Streamlit apps.

### Feel free to explore and extend this project to suit your needs!

   
