import re
import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
import seaborn as sns

nltk.download('stopwords')
nltk.download('wordnet')

def main():
    # open text files
    emailAlertWords = open("../01_Preprocessing/emailAlertWords.txt", "r")
    emailAlertWordsText = emailAlertWords.read()

    academicArticleWords = open("../01_Preprocessing/academicArticleWords.txt", "r")
    academicArticleWordsText = academicArticleWords.read()

    newsArticleWords = open("../01_Preprocessing/newsArticleWords.txt", "r")
    newsArticleWordsText = newsArticleWords.read()

    # use 'ngramRange' to decide how many words to group together
    ngramRange = 2
    ngramVal = "" # word to be displayed in plots

    if(ngramRange == 1):
        ngramVal = "Words"
    elif(ngramRange == 2):
        ngramVal = "Bigrams"
    elif(ngramRange == 3):
        ngramVal = "Trigrams"
    else:
        ngramVal = f"Groups of {ngramRange} Words"

    # preprocessing specifically necessary for TF-IDF
    emailAlertsTfidf = tfidfPreprocess(emailAlertWordsText, ngramRange)
    academicArticlesTfidf = tfidfPreprocess(academicArticleWordsText, ngramRange)
    newsArticlesTfidf = tfidfPreprocess(newsArticleWordsText, ngramRange)

    # merge docs (each compilation of source text types) into a single corpus for TF-IDF
    documents = [emailAlertsTfidf, academicArticlesTfidf, newsArticlesTfidf]
    documentNames = ["Email Alerts", "Academic Articles", "News Articles"]

    tfidf = TfidfVectorizer(ngram_range=(ngramRange, ngramRange))
    tfidfValues = tfidf.fit_transform(documents)
    featureNames = tfidf.get_feature_names_out()

    # convert matrix to coordinate format
    coordinateMatrix = tfidfValues.tocoo()

    # create a df with each word's tf-idf value for each document type
    tfidfDf = pd.DataFrame({
        "Document": [documentNames[doc] for doc in coordinateMatrix.row], # document name corresponding to index
        "Word": [featureNames[word] for word in coordinateMatrix.col],  # word corresponding to index
        "DocumentIndex": coordinateMatrix.row,
        "WordIndex": coordinateMatrix.col,
        "TfidfValue": coordinateMatrix.data
    })

    print(tfidfDf)
    tfidfDf.to_csv("tfidfScores.csv", index=False)

    # PLOT TOP <insert # here> WORDS (BASED ON TF-IDF SCORE) PER TYPE OF SOURCE TEXT
    topNumber = 50

    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(1, 3, figsize=(18, 8), sharey=False)

    for i, category in enumerate(documentNames):
        subset = tfidfDf[tfidfDf["Document"] == category].nlargest(topNumber, "TfidfValue")
        sns.barplot(data=subset, x="TfidfValue", y="Word", ax=axes[i], palette="rocket", hue="Word", legend=False)
        axes[i].set_title(f"Top {topNumber} {ngramVal} in {category}")
        axes[i].set_xlabel("TF-IDF Score")
        axes[i].set_ylabel("Words")

    plt.tight_layout()
    plt.show()

    # PLOT OVERALL TOP <insert # here> WORDS (BASED ON TF-IDF SCORE) ACROSS ALL SOURCE TEXTS
    topWordsDf = tfidfDf.nlargest(topNumber, "TfidfValue")
    print(topWordsDf)

    # Set figure size
    plt.figure(figsize=(14, 12))
    palette = sns.color_palette("rocket", n_colors=tfidfDf["Document"].nunique())

    # Create the stacked barplot - as of now, will be skewed based on which source texts we have more text
    sns.barplot(
        data=topWordsDf,
        x="TfidfValue",
        y="Word",
        hue="Document",
        dodge=False,
        palette=palette
    )

    # Add legend
    plt.legend(title="Document Category")

    # Labels and title
    plt.xlabel("TF-IDF Score")
    plt.ylabel("Word")
    plt.title(f"Top 50 {ngramVal} by TF-IDF Score")

    # Show plot
    plt.show()

def tfidfPreprocess(text, ngramRange):
    # remove punctuation, words that are <= 2 characters long
    # some 'words' pop up that are either abbreviations for things or were part of some numerical value unit and are therefore unnecessary
    noPunctuation = re.sub(r'[^\w\s]|\s\w{1,2}\s', '', text)

    # initialize object for lemmatization
    wnl = WordNetLemmatizer()

    # remove stop words + customized list of words that are common but unimportant for our purposes
    stopWords = set(stopwords.words('english'))
    #print("STOP WORDS")
    stopWords = stopWords.union(['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'monday', 'tuesday', 'wednesday', 'friday', 'copyright', 'also', 'that', 'hathaway', 'doug', 'biesecker'])
    #print(stopWords)

    wordTokens = word_tokenize(noPunctuation)
    # only keep words that are not stop words; lemmatize each word during the process
    filteredSentence = [wnl.lemmatize(w) for w in wordTokens if not w in stopWords]

    # Join the filtered words to form a clean text
    cleanText = ' '.join(filteredSentence)
    return cleanText

    #print(wordTokens)
    #print(filteredSentence)

main()