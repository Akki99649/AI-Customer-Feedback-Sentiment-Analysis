def get_emotion(result):

    emotion = result.get(
        "emotion",
        "Unknown"
    )

    if not emotion:

        return "Unknown"

    return str(
        emotion
    ).strip()