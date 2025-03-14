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
import matplotlib.colors as mcolors
import matplotlib.cm as cm
import seaborn as sns

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

    # preprocessing specifically necessary for single word, bigram and trigram analysis
    emailAlertsTfidf = wordAnalysisPreprocess(emailAlertWordsText)
    academicArticlesTfidf = wordAnalysisPreprocess(academicArticleWordsText)
    newsArticlesTfidf = wordAnalysisPreprocess(newsArticleWordsText)

    # TF-IDF ANALYSIS
    # merge docs (each compilation of source text types) into a single corpus for TF-IDF
    documents = [academicArticlesTfidf, emailAlertsTfidf, newsArticlesTfidf]
    documentNames = ["Academic Articles", "Email Alerts", "News Articles"]

    # use 'ngramRange' to decide how many words to group together
    ngramRange = 1
    ngramVal = ""  # word to be displayed in plots

    for i in range(1, 4):
        ngramRange = i

        if (ngramRange == 1):
            ngramVal = "Unigrams"
        elif (ngramRange == 2):
            ngramVal = "Bigrams"
        elif (ngramRange == 3):
            ngramVal = "Trigrams"
        else:
            ngramVal = f"Groups of {ngramRange} Words"

        tfidf = TfidfVectorizer(ngram_range=(ngramRange, ngramRange))
        tfidfValues = tfidf.fit_transform(documents)
        featureNames = tfidf.get_feature_names_out()

        # convert matrix to coordinate format
        coordinateMatrix = tfidfValues.tocoo()

        # create a df with each word's tf-idf value for each document type
        wordScoresDf = pd.DataFrame({
            "Document": [documentNames[doc] for doc in coordinateMatrix.row], # document name corresponding to index
            "Word": [featureNames[word] for word in coordinateMatrix.col],  # word corresponding to index
            "DocumentIndex": coordinateMatrix.row,
            "WordIndex": coordinateMatrix.col,
            "TfidfValue": coordinateMatrix.data
        })

        # PLOT TF-IDF DATA

        # WORD DIFFICULTY ANALYSIS
        # Source code: https://github.com/dusking/medium_src/tree/main/src
        # Article source: https://python.plainenglish.io/estimating-word-difficulty-in-english-using-machine-learning-ml-5d366c0f0700
        # less than .55 = easy, > .55 = hard
        if (ngramRange == 1):
            word_difficulty = WordDifficultyML()
            word_difficulty.set_model()

            wordScoresDf['WordDifficultyScore'] = wordScoresDf['Word'].apply(lambda x: word_difficulty.eval_word(x))
            wordScoresDf['WordDifficulty'] = np.where(wordScoresDf['WordDifficultyScore'] < .55, "easy", "hard")

        wordScoresDf.to_csv(f"{ngramRange}_wordScoresDf.csv", index=False)

        # PLOT TF-IDF, WORD DIFFICULTY DATA
        if (ngramRange == 1):
            plotAvgWordScores(wordScoresDf)
            plotOverallTopTfidf(60, ngramVal, wordScoresDf)

        plotTopNumPerSourceTfidf(20, ngramRange, ngramVal, wordScoresDf, documentNames)

def plotTopNumPerSourceTfidf(topNumber, ngramRange, ngramVal, wordScoresDf, documentNames):
    # PLOT TOP <insert # here> WORDS (BASED ON TF-IDF SCORE) PER TYPE OF SOURCE TEXT
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(1, 3, figsize=(22, 10), sharey=False)
    palette = sns.color_palette("flare", n_colors=wordScoresDf["Document"].nunique())

    for i, category in enumerate(documentNames):
        subset = wordScoresDf[wordScoresDf["Document"] == category].nlargest(topNumber, "TfidfValue").sort_values(by="Document", ascending=True).sort_values(by='TfidfValue', ascending=False)
        sns.barplot(data=subset, x="TfidfValue", y="Word", ax=axes[i], color=palette[i], legend=False)
        axes[i].set_xlim(0, wordScoresDf["TfidfValue"].max() * 1.1)
        axes[i].set_title(f"Top {topNumber} {ngramVal} (based on TF-IDF Score) in {category}")
        axes[i].set_xlabel("TF-IDF Score")
        axes[i].set_ylabel("Words")
        fig.tight_layout()

    plt.savefig(f"{ngramRange}_TopNumPerSourceTfidf.png", transparent=False)
    plt.show()

def plotAvgWordScores(wordScoresDf):
    # PLOT OVERALL TOP <insert # here> WORDS (BASED ON TF-IDF SCORE) ACROSS ALL SOURCE TEXTS
    avgWordDifficultyDf = pd.DataFrame(wordScoresDf.groupby("Document")["WordDifficultyScore"].mean())
    print(avgWordDifficultyDf)

    # Set figure size
    plt.figure(figsize=(18, 12))
    palette = sns.color_palette("flare", n_colors=wordScoresDf["Document"].nunique())

    # Create the stacked barplot - as of now, will be skewed based on which source texts we have more text
    sns.barplot(
        data=avgWordDifficultyDf,
        x="Document",
        y="WordDifficultyScore",
        hue="Document",
        palette=palette
    )

    # Labels and title
    plt.xlabel("Source Text Type")
    plt.ylabel("Word Difficulty Score")
    plt.title(f"Average Word Difficulty by Source Text Type")

    plt.savefig("AvgWordScores.png", transparent=False)
    plt.show()

def plotOverallTopTfidf(topNumber, ngramVal, wordScoresDf):
    fig, ax = plt.subplots(figsize=(18, 12))
    cmap = sns.color_palette("flare", as_cmap=True)

    sns.barplot(
        data=wordScoresDf.nlargest(topNumber, "TfidfValue").sort_values(by='WordDifficultyScore', ascending=True),
        x="TfidfValue",
        y="Word",
        hue="WordDifficultyScore",
        palette=cmap,
        #color = sns.color_palette("flare_r"),
        ax=ax,
        errorbar=None
    )

    ax.set_xlabel("TF-IDF Score")
    ax.set_ylabel("Word")
    ax.set_title(f"Top {topNumber} {ngramVal} by TF-IDF Score")

    # Remove the default legend
    ax.legend([], [], frameon=False)

    # Create a colorbar as a gradient legend
    norm = mcolors.Normalize(vmin=wordScoresDf["WordDifficultyScore"].min(),
                             vmax=wordScoresDf["WordDifficultyScore"].max())
    sm = cm.ScalarMappable(cmap=cmap.reversed(), norm=norm)
    sm.set_array([])

    cbar = fig.colorbar(sm, ax=ax, orientation="vertical")
    cbar.set_label("Word Difficulty")

    cbar.set_ticks([wordScoresDf["WordDifficultyScore"].min(), wordScoresDf["WordDifficultyScore"].max()])
    cbar.set_ticklabels(["Hard", "Easy"])

    plt.savefig("OverallTopTfidf.png", transparent=False)
    plt.show()

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
    stopWords = stopWords.union(['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'monday', 'tuesday', 'wednesday', 'friday', 'thats', 'said', 'also', 'copyright', 'one', 'two', 'three', 'would', 'within', 'yeah', 'dont', 'go'])

    wordTokens = word_tokenize(noPunctuation)
    # only keep words that are not stop words; lemmatize each word during the process
    filteredSentence = [wnl.lemmatize(w) for w in wordTokens if (not w in stopWords) and (w in words) and (not w in names)]

    # Join the filtered words to form a clean text
    cleanText = ' '.join(filteredSentence)
    return cleanText

main()