import pandas as pd
from transformers import pipeline

sentimentPipeline = pipeline("sentiment-analysis", model="ProsusAI/finbert") # allows for global use of pipeline

def main():
    emailAlertSentences = pd.read_csv("../01_Preprocessing/emailAlertSentences.csv").dropna()
    academicArticleSentences = pd.read_csv("../01_Preprocessing/academicArticleSentences.csv").dropna()
    newsArticleSentences = pd.read_csv("../01_Preprocessing/newsArticleSentences.csv").dropna()

    # Apply sentiment analysis function to each sentence
    emailAlertSentences[['SentimentLabel', 'SentimentScore']] = emailAlertSentences['Sentence'].apply(analyzeSentiment)
    academicArticleSentences[['SentimentLabel', 'SentimentScore']] = academicArticleSentences['Sentence'].apply(analyzeSentiment)
    newsArticleSentences[['SentimentLabel', 'SentimentScore']] = newsArticleSentences['Sentence'].apply(analyzeSentiment)

    emailAlertSentences.to_csv("emailAlertSentimentScores.csv", index=False)
    academicArticleSentences.to_csv("academicArticleSentimentScores.csv", index=False)
    newsArticleSentences.to_csv("newsArticleSentimentScores.csv", index=False)

def analyzeSentiment(sentence):
    print("sentence: ", sentence)
    result = sentimentPipeline(sentence)[0]
    print(result)
    return pd.Series([result['label'], result['score']])

main()