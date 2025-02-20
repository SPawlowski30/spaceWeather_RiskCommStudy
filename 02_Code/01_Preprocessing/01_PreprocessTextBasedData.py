from bs4 import BeautifulSoup
from pypdf import PdfReader
import requests

# EMAIL ALERTS
# update to look at all alerts from past 5 years...if that's possible?
forecastDiscussion = open('../../01_Data/Email_Alerts/ForecastDiscussion.txt', "r")
forecastDiscussionContent = forecastDiscussion.read()
print(forecastDiscussionContent)

# ACADEMIC ARTICLES
futureSpaceWeatherOpsResearch = PdfReader('../../01_Data/Academic_Articles/PlanningFutureSpaceWeatherOpsAndResearch.pdf')
for page in range(7, 108): # 7-108 are the actual desired pages; this excludes everything before preface and appendixes
    currPage = futureSpaceWeatherOpsResearch.pages[page]
    pageText = currPage.extract_text()
    print(pageText)

# NEWS ARTICLES
mitUrl = 'https://news.mit.edu/2013/space-weather-effects-on-satellites-0917'
mitArticle = requests.get(mitUrl)
mitArticleSoup = BeautifulSoup(mitArticle.text, 'html.parser')

# collect text only from the div that contains the body of the article; strip of HTML
for mitData in mitArticleSoup.find_all('div',{'class':'paragraph'}):
    print(mitData.text.strip())
    # TO-DO: split data into sentences, append each sentence to dataframe

