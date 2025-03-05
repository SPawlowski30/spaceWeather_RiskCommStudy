import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
import seaborn as sns

nltk.download('stopwords')

def main():
    # open text files
    emailAlertWords = open("../01_Preprocessing/emailAlertWords.txt", "r")
    emailAlertWordsText = emailAlertWords.read()

    academicArticleWords = open("../01_Preprocessing/academicArticleWords.txt", "r")
    academicArticleWordsText = academicArticleWords.read()

    newsArticleWords = open("../01_Preprocessing/newsArticleWords.txt", "r")
    newsArticleWordsText = newsArticleWords.read()

    # remove stop words from each text
    emailAlertsNoStopWords = removeStopWords(emailAlertWordsText)
    academicArticlesNoStopWords = removeStopWords(academicArticleWordsText)
    newsArticlesNoStopWords = removeStopWords(newsArticleWordsText)

    # merge docs into a single corpus for TF-IDF
    documents = [emailAlertsNoStopWords, academicArticlesNoStopWords, newsArticlesNoStopWords]
    documentNames = ["Email Alerts", "Academic Articles", "News Articles"]

    tfidf = TfidfVectorizer()
    tfidfValues = tfidf.fit_transform(documents)
    featureNames = tfidf.get_feature_names_out()

    # Convert sparse matrix to coordinate format
    coordinateMatrix = tfidfValues.tocoo()

    # Create a df with word indices and their corresponding words
    tfidfDf = pd.DataFrame({
        "Document": [documentNames[doc] for doc in coordinateMatrix.row], # Document name corresponding to index from list of document names
        "Word": [featureNames[word] for word in coordinateMatrix.col],  # Word corresponding to index
        "DocumentIndex": coordinateMatrix.row,
        "WordIndex": coordinateMatrix.col,
        "TfidfValue": coordinateMatrix.data
    })

    print(tfidfDf)

    # PLOT TOP WORDS PER DOCUMENT
    topNumber = 40

    # Set style
    sns.set_theme(style="whitegrid")

    # Create subplots
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=False)

    # Define categories
    categories = ["Email Alerts", "Academic Articles", "News Articles"]

    # Plot histograms
    for i, category in enumerate(categories):
        subset = tfidfDf[tfidfDf["Document"] == category].nlargest(topNumber, "TfidfValue")
        sns.barplot(data=subset, x="TfidfValue", y="Word", ax=axes[i], palette="rocket", hue="Word", legend=False)
        axes[i].set_title(f"Top {topNumber} Words in {category}")
        axes[i].set_xlabel("TF-IDF Score")
        axes[i].set_ylabel("Words")

    plt.tight_layout()
    plt.show()

def removeStopWords(text):
    stopWords = set(stopwords.words('english'))

    wordTokens = word_tokenize(text)
    filteredSentence = []

    for w in wordTokens:
        if w not in stopWords:
            filteredSentence.append(w)

    # Join the filtered words to form a clean text
    cleanText = ' '.join(filteredSentence)
    return cleanText

    #print(wordTokens)
    #print(filteredSentence)

main()