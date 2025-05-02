import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    academicArticleSentimentValues = pd.read_csv("../../../02_Code/03_Sentiment_Scores/academicArticleSentimentScores.csv")
    emailAlertSentimentValues = pd.read_csv("../../../02_Code/03_Sentiment_Scores/emailAlertSentimentScores.csv")
    newsArticleSentimentValues = pd.read_csv("../../../02_Code/03_Sentiment_Scores/newsArticleSentimentScores.csv")
    dashboardSentimentValues = pd.read_csv("../../../02_Code/03_Sentiment_Scores/dashboardSentimentScores.csv")

    sentimentScoresDf = pd.concat([emailAlertSentimentValues, academicArticleSentimentValues, newsArticleSentimentValues, dashboardSentimentValues])
    sentimentCounts = sentimentScoresDf.groupby(["SourceTextType"])["SentimentLabel"].value_counts().reset_index(name="Count")
    sentimentCounts["Proportion"] = sentimentCounts["Count"] / sentimentCounts.groupby("SourceTextType")[
        "Count"].transform("sum")

    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(2, 2, figsize=(18, 12), sharey=False)
    axes = axes.flatten()

    palette = sns.color_palette("flare", n_colors=sentimentCounts["SentimentLabel"].nunique())

    graphOrder = ["emailAlert", "academicArticle", "newsArticle", "DashboardMessages"]
    pieTitles = ["Email Alerts", "Academic Articles", "News Articles", "Dashboard Messages"]
    sentimentCounts["SourceTextType"] = pd.Categorical(sentimentCounts["SourceTextType"], categories=graphOrder, ordered=True)
    sentimentCounts = sentimentCounts.sort_values("SourceTextType")

    for i, category in enumerate(graphOrder):
        subset = sentimentCounts[sentimentCounts["SourceTextType"] == category]
        wedges, texts, autotexts = axes[i].pie(data=subset, x="Proportion", colors=palette, autopct="%1.1f%%", pctdistance=1.25)
        axes[i].set_title(f"{pieTitles[i]}", fontsize=24, pad=20)
        axes[i].set_xlabel("", fontsize=24) # No need for x label, the graph is self-explanatory

        # Set percent font size
        for autotext in autotexts:
            autotext.set_fontsize(24)

        # Grab colors from first plot for legend (if last legend is used, Positive does not show up since it doesn't exist for dashboardMessages)
        if category == "emailAlert":
            legendWedges = wedges

        fig.tight_layout()
        # Padding between columns so that titles don't overlap
        fig.subplots_adjust(wspace=0.1)

    plt.legend(
        handles=legendWedges,
        labels=["Neutral", "Negative", "Positive"],
        loc = "center",
        ncol=1,
        bbox_to_anchor=(-.4, 1),
        frameon=False,
        borderaxespad=0.0,
        title="Sentiment Label",
        prop={"size": 24},
        title_fontsize=24)
    plt.savefig("sentimentProportionsBySourceTextType.png")
    plt.show()

main()