import pandas as pd


# ---------------------------------------------------------
# VALIDATE FEEDBACK
# ---------------------------------------------------------

def validate_feedback(feedback):

    if feedback is None:

        return False

    if not isinstance(
        feedback,
        str
    ):

        return False

    feedback = feedback.strip()

    if len(feedback) < 5:

        return False

    return True


# ---------------------------------------------------------
# CONVERT RESULTS TO DATAFRAME
# ---------------------------------------------------------

def results_to_dataframe(results):

    rows = []

    for result in results:

        rows.append(
            {
                "feedback":
                    result.get(
                        "feedback",
                        ""
                    ),

                "sentiment":
                    result.get(
                        "sentiment",
                        ""
                    ),

                "emotion":
                    result.get(
                        "emotion",
                        ""
                    ),

                "keywords":
                    ", ".join(
                        result.get(
                            "keywords",
                            []
                        )
                    ),

                "topics":
                    ", ".join(
                        result.get(
                            "topics",
                            []
                        )
                    ),

                "main_complaint":
                    result.get(
                        "main_complaint",
                        ""
                    ),

                "summary":
                    result.get(
                        "summary",
                        ""
                    ),

                "satisfaction_score":
                    result.get(
                        "satisfaction_score",
                        0
                    ),

                "recommended_action":
                    result.get(
                        "recommended_action",
                        ""
                    ),

                "support_reply":
                    result.get(
                        "support_reply",
                        ""
                    )
            }
        )

    return pd.DataFrame(
        rows
    )


# ---------------------------------------------------------
# CREATE CSV DOWNLOAD
# ---------------------------------------------------------

def create_download_file(
    dataframe
):

    return dataframe.to_csv(
        index=False
    ).encode(
        "utf-8"
    )