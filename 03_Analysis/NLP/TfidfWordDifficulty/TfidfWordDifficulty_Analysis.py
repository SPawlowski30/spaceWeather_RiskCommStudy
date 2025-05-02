from scipy import stats

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm as cm
import seaborn as sns

def main():
    tfidf1Df = pd.read_csv("../../../02_Code/02_Tfidf_WordDifficulty_Scores/1_tfidfDf.csv")

    tfidf2Df = pd.read_csv("../../../02_Code/02_Tfidf_WordDifficulty_Scores/2_tfidfDf.csv")

    tfidf3Df = pd.read_csv("../../../02_Code/02_Tfidf_WordDifficulty_Scores/3_tfidfDf.csv")

    wordDifficultyDf = pd.read_csv("../../../02_Code/02_Tfidf_WordDifficulty_Scores/wordDifficultyDf.csv")

    # TF-IDF ANALYSIS
    documentNames = ["Academic Articles", "Email Alerts", "News Articles"]
    plt.rcParams.update({'font.size': 24})

    # use 'ngramRange' to decide how many words to group together
    ngramRange = 0
    ngramVal = ""  # word to be displayed in plots

    for i in range(1, 4):
        ngramRange = i

        if ngramRange == 1:
            ngramVal = "Unigrams"
            plotAvgWordScores(wordDifficultyDf)
            plotOverallTopTfidf(60, ngramVal, tfidf1Df)
        elif ngramRange == 2:
            ngramVal = "Bigrams"
        else :
            ngramVal = "Trigrams"

        plotTopNumPerSourceTfidf(20, ngramRange, ngramVal, tfidf2Df, documentNames)
        palette = sns.color_palette("flare")
        print("Color Palette for Flare")
        print(palette.as_hex())

def plotTopNumPerSourceTfidf(topNumber, ngramRange, ngramVal, wordScoresDf, documentNames):
    # PLOT TOP <insert # here> WORDS (BASED ON TF-IDF SCORE) PER TYPE OF SOURCE TEXT
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(1, 3, figsize=(50, 10), sharey=False)
    palette = sns.color_palette("flare", n_colors=wordScoresDf["Document"].nunique())
    graphOrder = ["Email Alerts", "Academic Articles", "News Articles"]
    wordScoresDf["Document"] = pd.Categorical(wordScoresDf["Document"], categories=graphOrder,
                                         ordered=True)
    print(wordScoresDf)

    for i, category in enumerate(graphOrder):
        subset = wordScoresDf[wordScoresDf["Document"] == category].nlargest(topNumber, "TfidfValue").sort_values(by="Document").sort_values(by='TfidfValue', ascending=False)
        print("SUBSET")
        print(subset)
        sns.barplot(data=subset, x="TfidfValue", y="Word", ax=axes[i], color=palette[i], legend=False, alpha=1, saturation=1)
        axes[i].set_xlim(0, wordScoresDf["TfidfValue"].max() * 1.01)
        axes[i].set_title(f"Top {topNumber} {ngramVal} (based on TF-IDF Score) in {category}", fontsize=24)
        axes[i].set_xlabel("TF-IDF Score", fontsize=24)
        axes[i].set_ylabel("Words", fontsize=24)
        axes[i].tick_params(axis='y', labelsize=24)
        axes[i].tick_params(axis='x', labelsize=24)
        fig.tight_layout()
    plt.savefig(f"{ngramRange}_TopNumPerSourceTfidf.png", transparent=False)
    plt.show()

def plotAvgWordScores(wordScoresDf):
    # PLOT OVERALL TOP <insert # here> WORDS (BASED ON TF-IDF SCORE) ACROSS ALL SOURCE TEXTS
    avgWordDifficultyDf = pd.DataFrame(wordScoresDf.groupby("Document", as_index=False)["WordDifficultyScore"].mean().sort_values(by="WordDifficultyScore", ascending=False))
    print("AVERAGE WORD DIFFICULTY SCORES")
    print(avgWordDifficultyDf)

    print("T-TEST")
    tStat, pValue = stats.ttest_ind(wordScoresDf[wordScoresDf["Document"]=="Email Alerts"]["WordDifficultyScore"], wordScoresDf[wordScoresDf["Document"]=="Dashboard"]["WordDifficultyScore"])

    print(f"T-statistic: {tStat:.2f}")
    print(f"P-value: {pValue:.4f}")
    # Set figure size
    plt.figure(figsize=(18, 12))
    #palette = sns.color_palette("flare", n_colors=wordScoresDf["Document"].nunique())
    palette = sns.color_palette("flare")

    # Create the stacked barplot - as of now, will be skewed based on which source texts we have more text
    sns.barplot(
        data=avgWordDifficultyDf,
        x="Document",
        y="WordDifficultyScore",
        hue="Document",
        color=palette[4],
        saturation=1
    )

    # Labels and title
    plt.xlabel("Source Text Type")
    plt.ylabel("Word Difficulty Score")
    plt.title(f"Average Word Difficulty by Source Text Type")

    plt.savefig("AvgWordScores.png", transparent=False)
    plt.show()

def plotOverallTopTfidf(topNumber, ngramVal, wordScoresDf):
    fig, ax = plt.subplots(figsize=(20,25))
    cmap = sns.color_palette("flare", as_cmap=True)

    sns.barplot(
        data=wordScoresDf.nlargest(topNumber, "TfidfValue").sort_values(by='WordDifficultyScore', ascending=True),
        x="TfidfValue",
        y="Word",
        hue="WordDifficultyScore",
        palette=cmap,
        ax=ax,
        errorbar=None
    )

    ax.set_xlabel("TF-IDF Score", fontsize=24)
    ax.set_ylabel("Word", fontsize=24)
    ax.set_title(f"Top {topNumber} {ngramVal} by TF-IDF Score", fontsize=24)

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
    cbar.set_ticklabels(["Hard", "Easy"], fontsize=24)

    plt.savefig("OverallTopTfidf.png", transparent=False)
    plt.show()

main()