import streamlit as st
import re


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="NDA Risk Checker",
    page_icon="⚖️",
    layout="wide"
)

bg = "#f5f7fb"
bg_alt = "#edf3ff"
panel = "#ffffff"
panel_soft = "rgba(255, 255, 255, 0.85)"
text = "#0f172a"
text_muted = "#475569"
border = "rgba(148, 163, 184, 0.35)"
primary = "#2563eb"
primary_dark = "#1d4ed8"
shadow = "rgba(15, 23, 42, 0.08)"

st.markdown(
    f"""
    <style>
    :root {{
        --bg: {bg};
        --bg-alt: {bg_alt};
        --panel: {panel};
        --panel-soft: {panel_soft};
        --text: {text};
        --text-muted: {text_muted};
        --border: {border};
        --primary: {primary};
        --primary-dark: {primary_dark};
        --shadow: {shadow};
    }}

    html, body, .stApp, [data-testid="stAppViewContainer"] {{
        background: var(--bg);
        color: var(--text);
    }}

    .stApp {{
        background: radial-gradient(circle at top left, var(--bg-alt) 0%, var(--bg) 32%, var(--bg) 100%);
        color: var(--text);
    }}

    .block-container {{
        max-width: 1180px;
        padding-top: 4rem !important;
        padding-bottom: 4rem;
    }}

    .hero-box {{
        background: linear-gradient(135deg, #0f172a 0%, #162b4e 45%, var(--primary-dark) 100%);
        border-radius: 24px;
        padding: 2rem 2.2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 18px 45px var(--shadow);
        border: 1px solid var(--border);
    }}

    .hero-small {{
        color: #bfdbfe;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
    }}

    .hero-title {{
        color: #ffffff;
        font-size: clamp(2.1rem, 4vw, 3.2rem);
        line-height: 1.08;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }}

    .hero-description {{
        color: #dbeafe;
        font-size: 1.02rem;
        line-height: 1.6;
        max-width: 760px;
    }}

    .stButton > button {{
        border-radius: 12px;
        font-weight: 700;
        min-height: 48px;
        background: linear-gradient(135deg, var(--primary), var(--primary-dark));
        color: white;
        border: none;
        box-shadow: 0 10px 25px rgba(37, 99, 235, 0.25);
    }}

    .stButton > button:hover {{
        background: linear-gradient(135deg, var(--primary-dark), #1e40af);
        color: white;
    }}

    [data-testid="stFileUploader"] section,
    .stTextArea textarea,
    .stTextInput input,
    .stSelectbox select,
    .stNumberInput input,
    .stMetric {{
        background: var(--panel-soft) !important;
        color: var(--text) !important;
        border: 1px solid var(--border) !important;
        border-radius: 14px !important;
    }}

    .stTextArea textarea,
    .stTextInput input,
    .stSelectbox select,
    .stNumberInput input {{
        box-shadow: none !important;
    }}

    [data-testid="stFileUploader"] section {{
        box-shadow: 0 10px 25px var(--shadow);
    }}

    .stMetric {{
        background: var(--panel) !important;
        border-radius: 18px;
        box-shadow: 0 8px 20px var(--shadow);
    }}

    .stAlert {{
        border-radius: 16px;
        border: none;
    }}

    p, li, div, span, label {{
        color: var(--text);
    }}

    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
    .stMarkdown p, .stMarkdown li {{
        color: var(--text);
    }}

    div[data-testid="stVerticalBlock"] > div:has(div[data-testid="stAlert"]) {{
        margin-top: 0.25rem;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="hero-box">
        <div class="hero-small">LEGAL TECHNOLOGY • NDA ANALYSIS</div>
        <div class="hero-title">NDA Risk Checker</div>
        <div class="hero-description">
            A lightweight contract-analysis prototype for identifying
            potential risks in non-disclosure agreements.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)



# ============================================================
# RISK ANALYSIS FUNCTIONS
# ============================================================

def check_liability_cap(text):

    patterns = [
        r"limitation of liability",
        r"limit(?:s|ed|ation)? of liability",
        r"liability.*cap",
        r"cap.*liability",
        r"maximum liability",
        r"aggregate liability",
        r"shall not exceed",
        r"liability.*shall not exceed"
    ]

    for pattern in patterns:

        if re.search(pattern, text, re.IGNORECASE):

            return {
                "level": "LOW",
                "status": "LOWER RISK",
                "finding": (
                    "A limitation or cap on liability appears "
                    "to be present."
                ),
                "details": (
                    "The agreement contains language that may "
                    "restrict the parties' liability."
                )
            }

    return {
        "level": "HIGH",
        "status": "POTENTIAL RISK",
        "finding": "No obvious liability cap was detected.",
        "details": (
            "The NDA may expose a party to potentially uncapped "
            "liability. The agreement should be reviewed to "
            "determine whether a liability limitation is appropriate."
        )
    }


def check_indemnification(text):

    indemnification_patterns = [
        r"indemnif",
        r"hold harmless",
        r"defend.*against",
        r"indemnity"
    ]

    broad_patterns = [
        r"any and all",
        r"all claims",
        r"any claims",
        r"any loss",
        r"all losses",
        r"any damages",
        r"all damages",
        r"without limitation"
    ]

    has_indemnification = any(
        re.search(pattern, text, re.IGNORECASE)
        for pattern in indemnification_patterns
    )

    has_broad_language = any(
        re.search(pattern, text, re.IGNORECASE)
        for pattern in broad_patterns
    )

    if has_indemnification and has_broad_language:

        return {
            "level": "HIGH",
            "status": "POTENTIAL RISK",
            "finding": "Broad indemnification language was detected.",
            "details": (
                "The agreement contains indemnification language "
                "combined with broad wording such as 'any and all'. "
                "The scope and limits of the indemnification obligation "
                "should be reviewed."
            )
        }

    if has_indemnification:

        return {
            "level": "MEDIUM",
            "status": "REVIEW",
            "finding": "An indemnification clause was detected.",
            "details": (
                "Indemnification is present, but the automated checker "
                "did not identify obviously broad wording."
            )
        }

    return {
        "level": "LOW",
        "status": "NO OBVIOUS ISSUE",
        "finding": "No indemnification clause was detected.",
        "details": (
            "No obvious indemnification provision was identified "
            "by the rule-based checker."
        )
    }


def check_confidentiality_definition(text):

    confidentiality_patterns = [
        r"confidential information",
        r"confidentiality",
        r"confidential"
    ]

    broad_patterns = [
        r"all information",
        r"any information",
        r"any and all information",
        r"information of any kind",
        r"information.*whether written or oral",
        r"without limitation"
    ]

    has_confidentiality = any(
        re.search(pattern, text, re.IGNORECASE)
        for pattern in confidentiality_patterns
    )

    has_broad_language = any(
        re.search(pattern, text, re.IGNORECASE)
        for pattern in broad_patterns
    )

    if has_confidentiality and has_broad_language:

        return {
            "level": "HIGH",
            "status": "POTENTIAL RISK",
            "finding": (
                "The definition of confidential information "
                "may be overly broad."
            ),
            "details": (
                "Broad wording was detected. Review whether the "
                "agreement clearly defines confidential information "
                "and contains appropriate exclusions."
            )
        }

    if has_confidentiality:

        return {
            "level": "MEDIUM",
            "status": "REVIEW",
            "finding": (
                "A confidentiality definition was detected."
            ),
            "details": (
                "The agreement contains a confidentiality definition, "
                "but its precise scope requires legal review."
            )
        }

    return {
        "level": "HIGH",
        "status": "POTENTIAL RISK",
        "finding": (
            "No clear definition of confidential information "
            "was detected."
        ),
        "details": (
            "The agreement should be reviewed to determine whether "
            "confidential information is adequately defined."
        )
    }


# ============================================================
# ANALYSE CONTRACT
# ============================================================

def analyse_contract(text):

    return {
        "Liability Cap": check_liability_cap(text),
        "Indemnification": check_indemnification(text),
        "Confidentiality Definition": check_confidentiality_definition(text)
    }


# ============================================================
# INPUT SECTION
# ============================================================

st.subheader("Upload or paste your NDA")

st.caption(
    "Provide the contract text below. The prototype will check "
    "three specific contractual risk areas."
)


uploaded_file = st.file_uploader(
    "Upload a .txt file",
    type=["txt"]
)


contract_text = ""


if uploaded_file is not None:

    try:

        contract_text = uploaded_file.getvalue().decode("utf-8")

        st.success("NDA uploaded successfully.")

    except UnicodeDecodeError:

        st.error(
            "The file could not be read. Please use a UTF-8 .txt file."
        )

else:

    contract_text = st.text_area(
        "Paste NDA text",
        height=260,
        placeholder="Paste the NDA text here..."
    )


# ============================================================
# ANALYSE BUTTON
# ============================================================

analyse_button = st.button(
    "Analyse NDA",
    type="primary",
    use_container_width=True
)


# ============================================================
# RESULTS
# ============================================================

if analyse_button:

    if not contract_text.strip():

        st.error(
            "Please upload or paste an NDA before analysing it."
        )

    else:

        results = analyse_contract(contract_text)

        st.divider()

        st.subheader("Risk assessment")

        st.caption(
            "Automated screening of three contractual risk areas."
        )


        # ====================================================
        # SUMMARY
        # ====================================================

        high_risks = sum(
            1
            for result in results.values()
            if result["level"] == "HIGH"
        )

        medium_risks = sum(
            1
            for result in results.values()
            if result["level"] == "MEDIUM"
        )

        low_risks = sum(
            1
            for result in results.values()
            if result["level"] == "LOW"
        )


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Potential risks",
                high_risks,
                border=True
            )


        with col2:

            st.metric(
                "Requires review",
                medium_risks,
                border=True
            )


        with col3:

            st.metric(
                "No obvious issue",
                low_risks,
                border=True
            )


        st.write("")


        # ====================================================
        # RISK RESULTS
        # ====================================================

        for risk_name, result in results.items():

            with st.container(border=True):

                st.markdown(f"### {risk_name}")

                if result["level"] == "HIGH":

                    st.error(
                        f"⚠️ {result['status']}"
                    )

                elif result["level"] == "MEDIUM":

                    st.warning(
                        f"⚠️ {result['status']}"
                    )

                else:

                    st.success(
                        f"✓ {result['status']}"
                    )


                st.markdown("**Finding**")

                st.write(result["finding"])


                st.markdown("**Assessment**")

                st.write(result["details"])


        # ====================================================
        # DISCLAIMER
        # ====================================================

        st.info(
            """
            **Legal disclaimer**

            This application is a portfolio prototype using
            rule-based text analysis. It identifies potential
            contractual issues but does not provide legal advice,
            determine enforceability, or replace review by a
            qualified legal professional.
            """
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "NDA Risk Checker • Legal Technology Portfolio Project"
)
