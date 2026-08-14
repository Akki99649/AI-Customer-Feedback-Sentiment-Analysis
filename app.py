import streamlit as st
import pandas as pd
import plotly.express as px

from feedback_loader import (
    extract_feedback_from_file,
    load_csv_feedback
)
from llm_handler import analyze_feedback
from sentiment_analyzer import get_sentiment
from emotion_detector import get_emotion
from topic_extractor import get_keywords, get_topics
from utils import (
    validate_feedback,
    results_to_dataframe,
    create_download_file
)


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI Customer Feedback Analyzer",
    page_icon="🤖",
    layout="wide"
)


# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------

st.markdown(
    """
    <style>
    .main-title {
        font-size: 40px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 30px;
    }

    .result-card {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #ddd;
        margin-bottom: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown(
    '<div class="main-title">🤖 AI Customer Feedback & Sentiment Analysis</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Analyze customer sentiment, emotions, issues, satisfaction and recommended actions using AI.'
    '</div>',
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.header(" Options")

    analysis_mode = st.radio(
        "Choose analysis mode:",
        [
            "Single Feedback",
            "Bulk CSV Analysis"
        ]
    )

    st.divider()

    st.info(
        """
        **Week 5 AI Internship Project**

        Features:
        - Sentiment analysis
        - Emotion detection
        - Keyword extraction
        - Topic extraction
        - Complaint identification
        - Satisfaction score
        - AI support response
        - Bulk analysis
        - Dashboard
        """
    )


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = []


# =========================================================
# SINGLE FEEDBACK MODE
# =========================================================

if analysis_mode == "Single Feedback":

    st.header("📝 Analyze Customer Feedback")

    input_method = st.radio(
        "Select input method:",
        [
            "Enter Feedback",
            "Upload File"
        ],
        horizontal=True
    )

    feedback_text = ""

    # -----------------------------------------------------
    # MANUAL INPUT
    # -----------------------------------------------------

    if input_method == "Enter Feedback":

        feedback_text = st.text_area(
            "Enter customer feedback:",
            height=220,
            placeholder=(
                "Example:\n"
                "I ordered a laptop last week. It arrived late and "
                "the package was damaged. Customer support took "
                "two days to respond."
            )
        )

    # -----------------------------------------------------
    # FILE UPLOAD
    # -----------------------------------------------------

    else:

        uploaded_file = st.file_uploader(
            "Upload TXT, PDF or CSV file",
            type=["txt", "pdf", "csv"]
        )

        if uploaded_file is not None:

            try:

                feedback_text = extract_feedback_from_file(
                    uploaded_file
                )

                if feedback_text:

                    st.success(
                        f"Successfully loaded: {uploaded_file.name}"
                    )

                    with st.expander("View extracted feedback"):

                        st.write(feedback_text)

            except Exception as e:

                st.error(
                    f"Could not read the uploaded file: {e}"
                )

    # -----------------------------------------------------
    # ANALYZE BUTTON
    # -----------------------------------------------------

    if st.button(
        "🔍 Analyze Feedback",
        type="primary",
        use_container_width=True
    ):

        if not validate_feedback(feedback_text):

            st.warning(
                "Please enter or upload valid customer feedback."
            )

        else:

            with st.spinner(
                " AI is analyzing the customer feedback..."
            ):

                try:

                    result = analyze_feedback(
                        feedback_text
                    )

                    if "error" in result:

                        st.error(result["error"])

                    else:

                        st.session_state.analysis_results = [
                            result
                        ]

                        st.success(
                            "Analysis completed successfully!"
                        )

                        # ---------------------------------
                        # MAIN METRICS
                        # ---------------------------------

                        st.subheader(" Analysis Overview")

                        col1, col2, col3, col4 = st.columns(4)

                        sentiment = get_sentiment(result)
                        emotion = get_emotion(result)

                        score = result.get(
                            "satisfaction_score",
                            0
                        )

                        col1.metric(
                            "Sentiment",
                            sentiment
                        )

                        col2.metric(
                            "Primary Emotion",
                            emotion
                        )

                        col3.metric(
                            "Satisfaction",
                            f"{score}/10"
                        )

                        col4.metric(
                            "Topics",
                            len(get_topics(result))
                        )

                        st.divider()

                        # ---------------------------------
                        # SUMMARY
                        # ---------------------------------

                        st.subheader(" Summary")

                        st.write(
                            result.get(
                                "summary",
                                "No summary available."
                            )
                        )

                        # ---------------------------------
                        # COMPLAINT
                        # ---------------------------------

                        st.subheader("⚠️ Main Complaint / Issue")

                        st.write(
                            result.get(
                                "main_complaint",
                                "No major complaint identified."
                            )
                        )

                        # ---------------------------------
                        # KEYWORDS + TOPICS
                        # ---------------------------------

                        col1, col2 = st.columns(2)

                        with col1:

                            st.subheader("🔑 Keywords")

                            keywords = get_keywords(
                                result
                            )

                            if keywords:

                                for keyword in keywords:

                                    st.markdown(
                                        f"- `{keyword}`"
                                    )

                            else:

                                st.write(
                                    "No keywords identified."
                                )

                        with col2:

                            st.subheader(" Topics")

                            topics = get_topics(
                                result
                            )

                            if topics:

                                for topic in topics:

                                    st.markdown(
                                        f"- {topic}"
                                    )

                            else:

                                st.write(
                                    "No topics identified."
                                )

                        st.divider()

                        # ---------------------------------
                        # RECOMMENDED ACTION
                        # ---------------------------------

                        st.subheader(
                            " Recommended Support Action"
                        )

                        st.info(
                            result.get(
                                "recommended_action",
                                "No recommendation available."
                            )
                        )

                        # ---------------------------------
                        # SUPPORT REPLY
                        # ---------------------------------

                        st.subheader(
                            " Suggested Customer Support Reply"
                        )

                        st.success(
                            result.get(
                                "support_reply",
                                "No support reply generated."
                            )
                        )

                        # ---------------------------------
                        # FULL JSON
                        # ---------------------------------

                        with st.expander(
                            " View Complete AI Analysis"
                        ):

                            st.json(result)

                except Exception as e:

                    st.error(
                        f"Unexpected error: {e}"
                    )


# =========================================================
# BULK CSV MODE
# =========================================================

else:

    st.header(" Bulk Customer Feedback Analysis")

    st.write(
        "Upload a CSV file containing a column named "
        "`feedback`."
    )

    uploaded_csv = st.file_uploader(
        "Upload CSV dataset",
        type=["csv"]
    )

    if uploaded_csv is not None:

        try:

            df = load_csv_feedback(
                uploaded_csv
            )

            st.success(
                f"Loaded {len(df)} feedback records."
            )

            st.dataframe(
                df,
                use_container_width=True
            )

            if st.button(
                " Analyze All Feedback",
                type="primary",
                use_container_width=True
            ):

                results = []

                progress_bar = st.progress(0)

                status_text = st.empty()

                for index, row in df.iterrows():

                    feedback = str(
                        row["feedback"]
                    )

                    status_text.write(
                        f"Analyzing feedback "
                        f"{index + 1}/{len(df)}..."
                    )

                    if validate_feedback(feedback):

                        try:

                            result = analyze_feedback(
                                feedback
                            )

                            if "error" not in result:

                                result["feedback"] = feedback

                                results.append(
                                    result
                                )

                        except Exception:

                            pass

                    progress_bar.progress(
                        (index + 1) / len(df)
                    )

                status_text.write(
                    "Analysis completed!"
                )

                if results:

                    st.session_state.analysis_results = results

                    results_df = results_to_dataframe(
                        results
                    )

                    st.subheader(
                        " Analysis Results"
                    )

                    st.dataframe(
                        results_df,
                        use_container_width=True
                    )

                    # ---------------------------------
                    # DOWNLOAD
                    # ---------------------------------

                    csv_data = create_download_file(
                        results_df
                    )

                    st.download_button(
                        label=" Download Results as CSV",
                        data=csv_data,
                        file_name="feedback_analysis_results.csv",
                        mime="text/csv"
                    )

                    st.divider()

                    # ---------------------------------
                    # DASHBOARD
                    # ---------------------------------

                    st.header(
                        " Customer Feedback Dashboard"
                    )

                    col1, col2, col3 = st.columns(3)

                    total_reviews = len(
                        results_df
                    )

                    average_score = round(
                        results_df[
                            "satisfaction_score"
                        ].mean(),
                        2
                    )

                    positive_count = (
                        results_df[
                            "sentiment"
                        ]
                        .str.lower()
                        .eq("positive")
                        .sum()
                    )

                    col1.metric(
                        "Total Reviews",
                        total_reviews
                    )

                    col2.metric(
                        "Average Satisfaction",
                        f"{average_score}/10"
                    )

                    col3.metric(
                        "Positive Reviews",
                        positive_count
                    )

                    # ---------------------------------
                    # SENTIMENT CHART
                    # ---------------------------------

                    sentiment_counts = (
                        results_df[
                            "sentiment"
                        ]
                        .value_counts()
                        .reset_index()
                    )

                    sentiment_counts.columns = [
                        "sentiment",
                        "count"
                    ]

                    fig_sentiment = px.bar(
                        sentiment_counts,
                        x="sentiment",
                        y="count",
                        title="Customer Sentiment Distribution",
                        labels={
                            "sentiment": "Sentiment",
                            "count": "Number of Reviews"
                        }
                    )

                    st.plotly_chart(
                        fig_sentiment,
                        use_container_width=True
                    )

                    # ---------------------------------
                    # EMOTION CHART
                    # ---------------------------------

                    emotion_counts = (
                        results_df[
                            "emotion"
                        ]
                        .value_counts()
                        .reset_index()
                    )

                    emotion_counts.columns = [
                        "emotion",
                        "count"
                    ]

                    fig_emotion = px.bar(
                        emotion_counts,
                        x="emotion",
                        y="count",
                        title="Customer Emotion Distribution"
                    )

                    st.plotly_chart(
                        fig_emotion,
                        use_container_width=True
                    )

                    # ---------------------------------
                    # SATISFACTION CHART
                    # ---------------------------------

                    fig_score = px.histogram(
                        results_df,
                        x="satisfaction_score",
                        nbins=10,
                        title="Customer Satisfaction Scores",
                        labels={
                            "satisfaction_score":
                            "Satisfaction Score"
                        }
                    )

                    st.plotly_chart(
                        fig_score,
                        use_container_width=True
                    )

                else:

                    st.warning(
                        "No valid feedback could be analyzed."
                    )

        except Exception as e:

            st.error(
                f"Could not process CSV file: {e}"
            )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "AI Customer Feedback & Sentiment Analysis System | "
    "Week 5 AI Internship Project"
)