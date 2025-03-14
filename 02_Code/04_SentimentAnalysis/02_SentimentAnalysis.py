import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    academicArticleSentimentValues = pd.read_csv("./academicArticleSentimentScores.csv")
    emailAlertSentimentValues = pd.read_csv("./emailAlertSentimentScores.csv")
    newsArticleSentimentValues = pd.read_csv("./newsArticleSentimentScores.csv")

    sentimentScoresDf = pd.concat([academicArticleSentimentValues, emailAlertSentimentValues, newsArticleSentimentValues])
    sentimentCounts = sentimentScoresDf.groupby(["SourceTextType"])["SentimentLabel"].value_counts().reset_index(name="Count")
    sentimentCounts["Proportion"] = sentimentCounts["Count"] / sentimentCounts.groupby("SourceTextType")[
        "Count"].transform("sum")

    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(1, 3, figsize=(22, 10), sharey=False)

    documentNames = sentimentCounts["SourceTextType"].unique()
    palette = sns.color_palette("flare", n_colors=sentimentCounts["SentimentLabel"].nunique())

    for i, category in enumerate(documentNames):
        subset = sentimentCounts[sentimentCounts["SourceTextType"] == category]
        axes[i].pie(data=subset, x="Proportion", colors=palette, autopct="%1.1f%%", pctdistance=1.15)
        axes[i].set_title(f"Sentence Sentiment Proportions for {category}")
        axes[i].set_xlabel("Proportion")
        fig.tight_layout()

    plt.legend(
        labels=["Neutral", "Negative", "Positive"],
        loc = "center",
        ncol=1,
        bbox_to_anchor=(0, 0),
        frameon=False,
        borderaxespad=0.0,
        title="Sentiment Label")
    plt.savefig("sentimentProportionsBySourceTextType.png")
    plt.show()

main()