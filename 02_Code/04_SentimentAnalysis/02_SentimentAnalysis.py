import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    academicArticleSentimentValues = pd.read_csv("./academicArticleSentimentScores.csv")
    emailAlertSentimentValues = pd.read_csv("./emailAlertSentimentScores.csv")
    newsArticleSentimentValues = pd.read_csv("./newsArticleSentimentScores.csv")
    dashboardSentimentValues = pd.read_csv("./dashboardSentimentScores.csv")

    sentimentScoresDf = pd.concat([emailAlertSentimentValues, academicArticleSentimentValues, newsArticleSentimentValues, dashboardSentimentValues])
    sentimentCounts = sentimentScoresDf.groupby(["SourceTextType"])["SentimentLabel"].value_counts().reset_index(name="Count")
    sentimentCounts["Proportion"] = sentimentCounts["Count"] / sentimentCounts.groupby("SourceTextType")[
        "Count"].transform("sum")

    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(4, 1, figsize=(15, 22), sharey=False)

    documentNames = sentimentCounts["SourceTextType"].unique()
    palette = sns.color_palette("flare", n_colors=sentimentCounts["SentimentLabel"].nunique())

    graphOrder = ["emailAlert", "academicArticle", "newsArticle", "DashboardMessages"]
    sentimentCounts["SourceTextType"] = pd.Categorical(sentimentCounts["SourceTextType"], categories=graphOrder, ordered=True)
    sentimentCounts = sentimentCounts.sort_values("SourceTextType")

    for i, category in enumerate(graphOrder):
        subset = sentimentCounts[sentimentCounts["SourceTextType"] == category]
        wedges, texts, autotexts = axes[i].pie(data=subset, x="Proportion", colors=palette, autopct="%1.1f%%", pctdistance=1.25)
        axes[i].set_title(f"Sentence Sentiment Proportions for {category}", fontsize=24, pad=20)
        axes[i].set_xlabel("", fontsize=24) # No need for x label, the graph is self-explanatory

        # Set percent font size
        for autotext in autotexts:
            autotext.set_fontsize(24)

        # Grab colors from first plot for legend (if last legend is used, Positive does not show up since it doesn't exist for dashboardMessages)
        if category == "emailAlert":
            legendWedges = wedges
        fig.tight_layout()

    plt.legend(
        handles=legendWedges,
        labels=["Neutral", "Negative", "Positive"],
        loc = "center",
        ncol=1,
        bbox_to_anchor=(-.6, .5),
        frameon=False,
        borderaxespad=0.0,
        title="Sentiment Label",
        prop={"size": 24},
        title_fontsize=24)
    plt.savefig("sentimentProportionsBySourceTextType.png")
    plt.show()

main()