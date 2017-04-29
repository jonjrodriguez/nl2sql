import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=UserWarning)
    from nltk.sentiment import SentimentIntensityAnalyzer

def determineNegativeSentiment(statement):
    sid = SentimentIntensityAnalyzer()
    sentiment = sid.polarity_scores(statement)

    return sentiment['neg']
