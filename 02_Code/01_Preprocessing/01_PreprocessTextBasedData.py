import pandas as pd
from bs4 import BeautifulSoup
from pypdf import PdfReader
import requests
import re
import nltk
nltk.download('words')
nltk.download('punkt_tab')
from nltk.corpus import stopwords
from nltk.corpus import words
from nltk.tokenize import sent_tokenize

def main():
    # EMAIL ALERTS (data type: .txt)
    # preprocess text files
    threeDayForecastClean = preprocessTextFile('../../01_Data/TextBasedData/Email_Alerts/Txt_Compiler/Txt_3_Day_Forecast.txt')
    alertsWarningsWatchClean = preprocessTextFile('../../01_Data/TextBasedData/Email_Alerts/Txt_Compiler/Txt_Alerts_Warnings_Watch.txt')
    forecastDiscussionClean = preprocessTextFile('../../01_Data/TextBasedData/Email_Alerts/Txt_Compiler/Txt_Forecast_Discussion.txt')
    solarGeophysicalActivity = preprocessTextFile('../../01_Data/TextBasedData/Email_Alerts/Txt_Compiler/Txt_Report_Forecast_Solar_Geophysical_Activity.txt')
    weeklyClean = preprocessTextFile('../../01_Data/TextBasedData/Email_Alerts/Txt_Compiler/Txt_The_Weekly.txt')

    # convert text files to dataframes
    threeDayForecastDf = splitSentencesToDataFrame(threeDayForecastClean, "3DayForecast", "txt")
    alertsWarningsWatchDf = splitSentencesToDataFrame(alertsWarningsWatchClean, "AlertsWarningsWatch", "txt")
    forecastDiscussionDf = splitSentencesToDataFrame(forecastDiscussionClean, "ForecastDiscussion", "txt")
    solarGeophysicalActivityDf = splitSentencesToDataFrame(solarGeophysicalActivity, "SolarGeophysicalActivity", "txt")
    weeklyDf = splitSentencesToDataFrame(weeklyClean, "Weekly", "txt")

    # vertically combine all text file dfs
    textFileSentences = pd.concat([threeDayForecastDf, alertsWarningsWatchDf, forecastDiscussionDf, solarGeophysicalActivityDf, weeklyDf])
    print(textFileSentences)

    # ACADEMIC ARTICLES (data type: .pdf)
    spaceWeatherOpsResearchText = compilePdfText('../../01_Data/TextBasedData/Academic_Articles/PlanningFutureSpaceWeatherOpsAndResearch.pdf', 7, 108)
    spaceWeatherOpsResearchClean = standardPreprocess(spaceWeatherOpsResearchText)
    spaceWeatherOpsResearchSentences = splitSentencesToDataFrame(spaceWeatherOpsResearchClean, "SpaceWeatherOpsResearch", "pdf")

    # NEWS ARTICLES (data type: url -> text with HTML)
    mitUrl = 'https://news.mit.edu/2013/space-weather-effects-on-satellites-0917'
    mitArticle = requests.get(mitUrl)
    mitArticleSoup = BeautifulSoup(mitArticle.text, 'html.parser')
    mitArticleFull = ""

    # collect text only from the div that contains the body of the article; strip of HTML
    for mitData in mitArticleSoup.find_all('div',{'class':'paragraph'}):
        mitArticleFull += mitData.text.strip()
        #print(mitData.text.strip())

    mitArticleClean = standardPreprocess(mitArticleFull)
    mitArticleSentences = splitSentencesToDataFrame(mitArticleClean, "MitNews", "url")

    # remove items in parentheses? lots of citations in some of these...
    # also some words end up getting meshed together...ex: "workshopcopyright" - should we remove words not in the english language?

def preprocessTextFile(path):
    textFile = open(path, "r")
    text = textFile.read()
    preprocessedText = standardPreprocess(text)
    textFile.close()
    return preprocessedText

def compilePdfText(path, startPage, endPage):
    pdf = PdfReader(path)
    text = ""
    for page in range(startPage, endPage):
        currPage = pdf.pages[page]
        pageText = currPage.extract_text()
        text += pageText

    return text

def splitSentencesToDataFrame(text, title, sourceTextType):
    # each row will contain a single sentence from the input text string
    sentences = nltk.sent_tokenize(text)
    df = pd.DataFrame({'Sentence': sentences, 'Title': title, 'SourceTextType': sourceTextType})
    return df

def standardPreprocess(text):
    # ensure that text is an all lowercase sentence
    preprocessedText = str(text.lower())

    # remove numeric values, URLS, and any other items that are not characters; remove rest of punctuation after split into sentences
    preprocessedText = re.sub(r'http\S+|https\S+|[^a-zA-Z\s.,;:!?\'\"()-]', '', preprocessedText)
    # remove excessive whitespace
    preprocessedText = re.sub(r'\s+', ' ', preprocessedText).strip()  # Remove excessive spaces

    # remove command characters: new line, tab, return
    patternsToRemove = ['\n', '\t', '\r']
    for pattern in patternsToRemove:
        preprocessedText = preprocessedText.replace(pattern, '')

    # remove stop words if length of 3 or less (4 maybe?); commented out for now because we want to test sentence encoding before + after
    # only do this if text is tokenized first
    #filtered_words = [w for w in preprocessedText if len(w) > 3 if not w in stopwords.words('english')]

    return preprocessedText

main()

