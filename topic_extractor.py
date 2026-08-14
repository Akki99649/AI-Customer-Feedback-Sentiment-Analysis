def get_keywords(result):

    keywords = result.get(
        "keywords",
        []
    )

    if not isinstance(
        keywords,
        list
    ):

        return []

    return [
        str(keyword).strip()
        for keyword in keywords
        if str(keyword).strip()
    ]


def get_topics(result):

    topics = result.get(
        "topics",
        []
    )

    if not isinstance(
        topics,
        list
    ):

        return []

    return [
        str(topic).strip()
        for topic in topics
        if str(topic).strip()
    ]