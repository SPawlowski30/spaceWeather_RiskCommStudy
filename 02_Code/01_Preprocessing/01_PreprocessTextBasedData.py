from bs4 import BeautifulSoup
from pypdf import PdfReader
import requests
import re
import nltk
from nltk.corpus import stopwords

def main():
    # EMAIL ALERTS (data type: .txt)
    #forecastDiscussion = open('../../01_Data/TextBasedData/Email_Alerts/ForecastDiscussion.txt', "r")
    #forecastDiscussionContent = forecastDiscussion.read()
    #print(forecastDiscussionContent)

    # ACADEMIC ARTICLES (data type: .pdf)
    futureSpaceWeatherOpsResearch = PdfReader('../../01_Data/TextBasedData/Academic_Articles/PlanningFutureSpaceWeatherOpsAndResearch.pdf')
    futureSpaceWeatherOpsResearchFull = ""

    for page in range(7, 108): # 7-108 are the actual desired pages; this excludes everything before preface and appendixes
        currPage = futureSpaceWeatherOpsResearch.pages[page]
        pageText = currPage.extract_text()

        futureSpaceWeatherOpsResearchFull += pageText
        #print(pageText)

    test = standardPreprocess(futureSpaceWeatherOpsResearchFull)
    print(test)

    # NEWS ARTICLES (data type: url -> text with HTML)
    mitUrl = 'https://news.mit.edu/2013/space-weather-effects-on-satellites-0917'
    mitArticle = requests.get(mitUrl)
    mitArticleSoup = BeautifulSoup(mitArticle.text, 'html.parser')
    mitArticleFull = ""

    # collect text only from the div that contains the body of the article; strip of HTML
    for mitData in mitArticleSoup.find_all('div',{'class':'paragraph'}):
        mitArticleFull += mitData.text.strip()
        #print(mitData.text.strip())

def standardPreprocess(text):
    # ensure that text is an all lowercase sentence
    preprocessedText = str(text.lower())

    # remove any URLs
    preprocessedText = re.sub(r'http\S+', '', preprocessedText)

    # remove numeric values and any other items that are not characters; remove rest of punctuation after split into sentences
    preprocessedText = re.sub(r'[^a-zA-Z\s.,;:!?\'\"()-]', '', preprocessedText)

    # remove command characters: new line, tab, return
    patternsToRemove = ['\n', '\t', '\r']
    for pattern in patternsToRemove:
        preprocessedText = preprocessedText.replace(pattern, '')

    # remove stop words if length of 3 or less (4 maybe?); commented out for now because we want to test sentence encoding before + after
    # only do this if text is tokenized first
    #filtered_words = [w for w in preprocessedText if len(w) > 3 if not w in stopwords.words('english')]

    return preprocessedText

main()

