import io
import pandas as pd

from pypdf import PdfReader


# ---------------------------------------------------------
# READ TEXT FILE
# ---------------------------------------------------------

def read_txt_file(uploaded_file):

    content = uploaded_file.read()

    return content.decode(
        "utf-8",
        errors="ignore"
    )


# ---------------------------------------------------------
# READ PDF FILE
# ---------------------------------------------------------

def read_pdf_file(uploaded_file):

    uploaded_file.seek(0)

    pdf_reader = PdfReader(
        uploaded_file
    )

    text = ""

    for page in pdf_reader.pages:

        page_text = page.extract_text()

        if page_text:

            text += page_text + "\n"

    return text.strip()


# ---------------------------------------------------------
# READ CSV FILE
# ---------------------------------------------------------

def read_csv_file(uploaded_file):

    uploaded_file.seek(0)

    df = pd.read_csv(
        uploaded_file
    )

    if "feedback" not in df.columns:

        raise ValueError(
            "CSV must contain a column named 'feedback'."
        )

    feedback_list = (
        df["feedback"]
        .dropna()
        .astype(str)
        .tolist()
    )

    return "\n\n".join(
        feedback_list
    )


# ---------------------------------------------------------
# EXTRACT FEEDBACK FROM FILE
# ---------------------------------------------------------

def extract_feedback_from_file(
    uploaded_file
):

    filename = uploaded_file.name.lower()

    if filename.endswith(".txt"):

        return read_txt_file(
            uploaded_file
        )

    elif filename.endswith(".pdf"):

        return read_pdf_file(
            uploaded_file
        )

    elif filename.endswith(".csv"):

        return read_csv_file(
            uploaded_file
        )

    else:

        raise ValueError(
            "Unsupported file format. "
            "Please upload TXT, PDF or CSV."
        )


# ---------------------------------------------------------
# LOAD CSV FOR BULK ANALYSIS
# ---------------------------------------------------------

def load_csv_feedback(
    uploaded_file
):

    uploaded_file.seek(0)

    df = pd.read_csv(
        uploaded_file
    )

    if "feedback" not in df.columns:

        raise ValueError(
            "CSV must contain a column named 'feedback'."
        )

    df = df[
        df["feedback"]
        .notna()
    ]

    df["feedback"] = (
        df["feedback"]
        .astype(str)
        .str.strip()
    )

    df = df[
        df["feedback"] != ""
    ]

    return df.reset_index(
        drop=True
    )