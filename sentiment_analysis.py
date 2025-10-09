from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Download for deployment
nltk.download('vader_lexicon', quiet=True)

# Initialize
vader = SentimentIntensityAnalyzer()

def classify_sentiment(text: str):
    """
    Returns:
        sentiment (str): 'positive', 'neutral', 'negative'
        polarity (float): -1.0 → 1.0
    """
    vader_scores = vader.polarity_scores(text)
    polarity = vader_scores["compound"]  # -1 to 1

    if polarity > 0.3:
        sentiment = "positive"
    elif polarity < -0.3:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return sentiment, polarity
