# review the comments using nlp and return the sentiment


from textblob import TextBlob

def analyze_sentiment(news_text):
    blob = TextBlob(news_text)
    sentiment = blob.sentiment.polarity
    if sentiment >60:
        return "Positive"
    elif sentiment < 30:
        return "Negative"
    else:
        return "Neutral"