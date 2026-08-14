def get_sentiment(result):

    sentiment = result.get(
        "sentiment",
        "Neutral"
    )

    sentiment = str(
        sentiment
    ).strip()

    if sentiment.lower() == "positive":

        return "Positive "

    elif sentiment.lower() == "negative":

        return "Negative "

    else:

        return "Neutral "