import streamlit as st
from streamlit_lottie import st_lottie
import boto3
import json

# Page config
st.set_page_config(
    page_title="📊 Financial Document Analyzer",
    layout="centered"
)

def load_lottieurl(url):
    import requests
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_json = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_jcikwtux.json")
st_lottie(lottie_json, height=200, key="analyze-animation")

# Title and description
st.title("📄 Financial Document Analyzer")
st.markdown("Upload your financial report PDF and get structured insights instantly.")

# Analysis goal selection
goal = st.selectbox("Choose analysis goal", [
    "Creditworthiness Analysis",
    "Failed Transactions RCA"
])

goal_to_mode = {
    "Creditworthiness Analysis": "credit_summary",
    "Failed Transactions RCA": "transaction_rca",
}

# File upload
uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])

# Analyze button
if uploaded_file is not None:
    if st.button("🔍 Analyze Document"):
        with st.spinner("Analyzing..."):
            try:
                # Read PDF as bytes
                pdf_bytes = uploaded_file.read()

                runtime = boto3.client("sagemaker-runtime", region_name="us-east-1")

                response = runtime.invoke_endpoint(
                    EndpointName="llm-backend-endpoint",
                    ContentType="application/json",  # or "application/octet-stream" depending on your model
                    Body=pdf_bytes  # or just pdf_bytes if the model accepts raw PDF
                )

                result_raw = response['Body'].read()
                print("result", result_raw)
                result = json.loads(result_raw).get("analysis", "No analysis returned.")

                st.success("✅ Analysis Complete")

                if goal_to_mode[goal] == "credit_summary":
                    st.subheader("📈 Creditworthiness Summary")
                    st.markdown(f"""
                    **🧮 Debt-to-Income Ratio:** `{result}`  
                    **📊 Credit Score:** `{result}`  
                    **⚠️ Risk Factors:**  
                    `{result}`
                    """, unsafe_allow_html=True)

                elif goal_to_mode[goal] == "transaction_rca":
                    st.subheader("💥 Transaction Failure Root Cause Analysis")
                    st.markdown(f"""
                    **📌 Key Facts:**  
                    `{result}`  
                    **🛠️ Root Cause:** `{result}`  
                    **💡 Recommendation:** `{result}`
                    """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ Failed to analyze document. Error: {e}")
