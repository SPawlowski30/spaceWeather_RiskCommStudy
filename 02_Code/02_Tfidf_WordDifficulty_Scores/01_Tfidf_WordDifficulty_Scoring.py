import re
import nltk
import numpy as np

from wordDifficulty.src.a05_word_difficulty_ml import WordDifficultyML
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('words')
nltk.download('names')

def main():
    academicArticleWords = open("../01_Preprocessing/academicArticleWords.txt", "r")
    academicArticleWordsText = academicArticleWords.read()

    emailAlertWords = open("../01_Preprocessing/emailAlertWords.txt", "r")
    emailAlertWordsText = emailAlertWords.read()

    newsArticleWords = open("../01_Preprocessing/newsArticleWords.txt", "r")
    newsArticleWordsText = newsArticleWords.read()

    dashboardWords = open("../01_Preprocessing/dashboardWords.txt", "r")
    dashboardWordsText = dashboardWords.read()

    # preprocessing specifically necessary for single word, bigram and trigram analysis
    emailAlertsClean = wordAnalysisPreprocess(emailAlertWordsText)
    academicArticlesClean = wordAnalysisPreprocess(academicArticleWordsText)
    newsArticlesClean = wordAnalysisPreprocess(newsArticleWordsText)
    dashboardClean = wordAnalysisPreprocess(dashboardWordsText)

    # TF-IDF ANALYSIS
    plt.rcParams.update({'font.size': 24})
    # merge docs (each compilation of source text types) into a single corpus for TF-IDF
    documents = [academicArticlesClean, emailAlertsClean, newsArticlesClean]
    documentNames = ["Academic Articles", "Email Alerts", "News Articles"]

    # use 'ngramRange' to decide how many words to group together
    ngramRange = 1
    ngramVal = ""  # word to be displayed in plots

    for i in range(1, 4):
        ngramRange = i

        tfidf = TfidfVectorizer(ngram_range=(ngramRange, ngramRange))
        tfidfValues = tfidf.fit_transform(documents)
        featureNames = tfidf.get_feature_names_out()

        # convert matrix to coordinate format
        coordinateMatrix = tfidfValues.tocoo()

        # create a df with each word's tf-idf value for each document type
        tfidfDf = pd.DataFrame({
            "Document": [documentNames[doc] for doc in coordinateMatrix.row], # document name corresponding to index
            "Word": [featureNames[word] for word in coordinateMatrix.col], # word corresponding to index
            "DocumentIndex": coordinateMatrix.row,
            "WordIndex": coordinateMatrix.col,
            "TfidfValue": coordinateMatrix.data
        })

        # WORD DIFFICULTY ANALYSIS
        # Source code: https://github.com/dusking/medium_src/tree/main/src
        # Article source: https://python.plainenglish.io/estimating-word-difficulty-in-english-using-machine-learning-ml-5d366c0f0700
        # less than .55 = easy, > .55 = hard
        if (ngramRange == 1):
            word_difficulty = WordDifficultyML()
            word_difficulty.set_model()

            # word difficulty for TfidfWordDifficulty
            tfidfDf['WordDifficultyScore'] = tfidfDf['Word'].apply(lambda x: word_difficulty.eval_word(x))
            tfidfDf['WordDifficulty'] = np.where(tfidfDf['WordDifficultyScore'] < .55, "easy", "hard")

            # Generate word difficulty DFs
            academicArticlesWordDifficulty = scoreWordDifficulty("Academic Articles", academicArticlesClean, word_difficulty)
            emailWordDifficulty = scoreWordDifficulty("Email Alerts", emailAlertsClean, word_difficulty)
            newsWordDifficulty = scoreWordDifficulty("News Articles", newsArticlesClean, word_difficulty)
            dashboardWordDifficulty = scoreWordDifficulty("Dashboard", dashboardClean, word_difficulty)

            # Combine for difficulty plot
            wordDifficultyDf = pd.concat([academicArticlesWordDifficulty, emailWordDifficulty, newsWordDifficulty, dashboardWordDifficulty], ignore_index=True)
            wordDifficultyDf.to_csv(f"wordDifficultyDf.csv", index=False)

        tfidfDf.to_csv(f"{ngramRange}_tfidfDf.csv", index=False)

def scoreWordDifficulty(sourceTextName, text, wordDifficultyAnalyzer):
    tokens = text.split()
    df = pd.DataFrame({"Document": sourceTextName, "Word": tokens})
    df["WordDifficultyScore"] = df["Word"].apply(lambda x: wordDifficultyAnalyzer.eval_word(x))
    df["WordDifficulty"] = np.where(df["WordDifficultyScore"] < .55, "easy", "hard")
    return df

def wordAnalysisPreprocess(text):
    # remove punctuation, words that are <= 2 characters long
    # some 'words' pop up that are either abbreviations for things or were part of some numerical value unit and are therefore unnecessary
    noPunctuation = re.sub(r'[^\w\s]|\s\w{1,2}\s', '', text)

    # initialize object for lemmatization
    wnl = WordNetLemmatizer()

    # remove stop words + customized list of words that are common but unimportant for our purposes
    stopWords = set(stopwords.words('english'))
    words = set(nltk.corpus.words.words())
    names = set(nltk.corpus.names.words())
    stopWords = stopWords.union(['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'monday', 'tuesday', 'wednesday', 'friday', 'thats', 'said', 'also', 'copyright', 'one', 'two', 'three', 'would', 'within', 'yeah', 'dont', 'go', 'threedayforecasttxt'])

    wordTokens = word_tokenize(noPunctuation)
    # only keep words that are not stop words; lemmatize each word during the process
    englishWordsOnly = [w for w in wordTokens if w in words]
    filteredSentence = [wnl.lemmatize(w) for w in englishWordsOnly if (not w in stopWords) and (w in words) and (not w in names)]

    # Join the filtered words to form a clean text
    cleanText = ' '.join(filteredSentence)
    return cleanText

main()