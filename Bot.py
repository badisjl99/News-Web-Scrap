import os
from nltk.corpus import stopwords
import webbrowser
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import requests
from collections import Counter
from lxml import html
import pandas as pd
from datetime import datetime
import time

urls = [
    'https://swentr.site', 
    'https://edition.cnn.com',
    'https://www.aljazeera.com',
    'https://www.france24.com/en/',
    'https://www.reuters.com',
    'https://www.dw.com/en/top-stories/s-9097',
    'https://www.theguardian.com/international',
    'https://www.cbsnews.com',
    'https://abcnews.go.com',
    'https://apnews.com',
    'https://news.sky.com/world',
    'https://www.euronews.com/news/international',
    'https://www.foxnews.com'
]

# Initialize a list to store the texts of all <span> tags with class 'main-promobox__link' and attribute 'data-editable="headline"'
span_texts = []

# Scrape each URL and extract the texts
for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    texts = []

    switch_url = {
        'https://swentr.site': ('span', {'class': 'main-promobox__link'}),
        'https://edition.cnn.com': ('span', {'data-editable': 'headline'}),
        'https://www.aljazeera.com': ('span', {}),
        'https://news.sky.com/world': ('span', {}),
        'https://www.france24.com/en/': ('p', {'class': 'article__title'}),
        'https://www.reuters.com': ('a', {'class': 'text__text__1FZLe text__dark-grey__3Ml43 text__medium__1kbOh text__heading_5_and_half__3YluN heading__base__2T28j heading_5_half media-story-card__heading__eqhp9'}),
        'https://www.dw.com/en/top-stories/s-9097': ('span', {}),
        'https://www.theguardian.com/international': ('a', {'class': 'u-faux-block-link__overlay js-headline-text'}),
        'https://www.cbsnews.com': ('h4', {'class': 'item__hed '}),
        'https://abcnews.go.com': (['h1', 'h2', 'h3', 'h4', 'h5', 'h6'], {}),
        'https://apnews.com': (['h1', 'h2', 'h3', 'h4', 'h5', 'h6'], {}),
        'https://www.independent.co.uk/news/world?CMP=ILC-refresh' :('a', {'class': 'title'})
    }

    tag, attributes = switch_url.get(url, (None, None))
    if tag is not None:
        spans = soup.find_all(tag, attributes)
        texts = [span.text.strip() for span in spans]
    span_texts.extend(texts)


# Combine all texts into a single string
texts_string = '\n\n'.join(span_texts)

# Your code here
stop_words = set(stopwords.words('english'))
specific_words = ["the", "and", "to", "of", "he", "was", "you","world", "man", "min", "by", "an", "has", "show",
                  "she", "it", "they", ".", "-", "never", "should", "have", "in", "is", "top",
                  "on", "a", "for", "new", "what", "us", "says", "his", "how", "as", "with",
                  "on", "about", "be", "million", "time", "this", "report", "–", "are", "record",
                  "after", "but", "that", "from", "at", "world's", "now", "we", "i'm","world"
                  "January", "February", "March", "April", "who", "may", "June", "July", "August",
                  "September", "October", "November", "December", "jazeera", "al", "2023", "section",
                  "next", "skip", "more", "ago", "hours", "over", "latest", "media", "why", "his", "her", "could", "still",
                  "first", "before"
                  ]

words = []
for text in span_texts:
    words.extend(text.split())

# Convert specific words to lowercase
specific_words = [word.lower() for word in specific_words]

words = [word.lower() for word in words if word.lower() not in stop_words and not word.isnumeric() and word.lower() not in specific_words]

# Filter out names with a certain length (optional)
names = [word for word in words if len(word) > 3]

word_counts = Counter(names)

# Get top 10 most frequent words
top_words = word_counts.most_common(15)
words, counts = zip(*top_words)
now = datetime.now()

# Format the date as 'dd/mm/YYYY'
date_string = now.strftime('%d/%m/%Y')

# Format the time as 'H:MMAM' or 'H:MMPM'
hour = now.strftime('%I').lstrip('0')
minute = now.strftime('%M')
am_pm = now.strftime('%p')
time_string = f"{hour}:{minute}{am_pm}"



# Save word counts to a file
filename = "word_counts.txt"

counter = 1
folder_name = f"Scrap{counter}"
while os.path.exists(folder_name):
    counter += 1
    folder_name = f"Scrap{counter}"
os.makedirs(folder_name)

# Get the current date and time
now = datetime.now()

# Format the date as 'dd/mm/YYYY'
date_string = now.strftime('%d/%m/%Y')

# Format the time as 'H:MMAM' or 'H:MMPM'
hour = now.strftime('%I').lstrip('0')
minute = now.strftime('%M')
am_pm = now.strftime('%p')
time_string = f"{hour}:{minute}{am_pm}"

# Define custom colors for the bars
colors = ['red', 'green', 'blue', 'orange', 'purple']

# Create the bar chart with colored bars
plt.bar(words, counts, color=colors)
plt.xlabel('Words')
plt.ylabel('Counts')
plt.title(f'Top 10 Most Frequent Words ({date_string} {time_string})')
plt.xticks(rotation=45)

# Save the bar chart to an image file in the created folder
chart_filename = os.path.join(folder_name, "bar_chart.png")
plt.savefig(chart_filename)
plt.close()

# Save word counts to a file in the created folder
filename = os.path.join(folder_name, "word_counts.txt")

# Write the word counts to the text file
with open(filename, 'w') as file:
    file.write(f"Top 10 Most Frequent Words:\n\n")
    for word, count in top_words:
        file.write(f"{word}: {count}\n")

# Print a message indicating that the scraping is complete and the results have been saved
print(f"Scraping completed successfully! Results saved to {folder_name}.")
print(f"Bar chart saved to {chart_filename}.")

