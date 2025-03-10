import pandas as pd
import matplotlib.pyplot as plt
from transformers import pipeline

def main():
    emailAlertSentences = pd.read_csv("../01_Preprocessing/emailAlertSentences.csv")
    academicArticleSentences = pd.read_csv("../01_Preprocessing/academicArticleSentences.csv")
    newsArticleSentences = pd.read_csv("../01_Preprocessing/newsArticleSentences.csv")

    #sentencesDf = pd.concat([emailAlertSentences, academicArticleSentences, newsArticleSentences], ignore_index=True)

    # Apply the function to each sentence
    emailAlertSentences[['Label', 'Score']] = emailAlertSentences['Sentence'].apply(analyzeSentiment)
    #sentencesDf.to_csv("SentimentScores.csv")
    emailAlertSentences.to_csv("emailAlertSentimentScores.csv")

def analyzeSentiment(sentence):
    # Load pre-trained sentiment analysis pipeline
    sentimentPipeline = pipeline("sentiment-analysis", model ="ProsusAI/finbert")

    result = sentimentPipeline(sentence)[0]
    print(result)
    return pd.Series([result['label'], result['score']])
main()