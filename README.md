# Financial_Document_Analyzer

## 🚀 About the Project
This project is a full-fledged **AI-powered Financial Document Analyzer** that allows users to upload financial PDFs and get structured insights instantly.
It was built to understand **real-world deployment practices** involving frontend, backend, and cloud services.

---

## 🛠 Tech Stack
- **Frontend:** Streamlit (deployed on AWS EC2)
- **Backend:** FastAPI (deployed via a custom Amazon SageMaker endpoint)
- **Model:** Hugging Face FLAN-T5
- **Cloud Services:** AWS EC2, SageMaker, IAM, CloudWatch
- **Other Libraries:** boto3, fitz (PyMuPDF), transformers

---

## ✨ Features
- Upload PDF financial reports
- Choose an analysis goal:
  - **Creditworthiness Analysis**
  - **Failed Transactions Root Cause Analysis**
- AI extracts key insights and recommendations
- Instant feedback with a clean and interactive frontend
- Fully deployed in a production-like cloud environment

---

## 📈 Deployment Architecture
```plaintext
User → Streamlit Frontend (EC2) → FastAPI Backend (SageMaker Endpoint) → FLAN-T5 Model → Results
```
- EC2 hosts the frontend app.
- FastAPI server hosted on SageMaker endpoint processes requests.
- Hugging Face model performs the text analysis.
- IAM roles and policies manage secure access.

---

## 🔥 How to Run Locally
### 1. Frontend (Streamlit)
```bash
pip install streamlit streamlit-lottie boto3
streamlit run app.py
```

### 2. Backend (FastAPI)
```bash
pip install fastapi uvicorn transformers pymupdf
uvicorn backend:app --host 0.0.0.0 --port 8000
```

Update the `boto3` credentials if running locally outside AWS.

---

## 📚 Learnings
- Deploying real-world AI apps using **AWS EC2, SageMaker, IAM, CloudWatch**
- Managing **frontend-backend** communication across cloud services
- Debugging issues like missing credentials, CORS, payload formatting
- Building production-grade APIs with **FastAPI**
- Handling PDFs, byte streams, and model payloads securely

---

## 🚧 Challenges Faced
- Configuring IAM permissions properly
- Debugging API errors hidden behind generic frontend messages
- Correctly handling file payloads and decoding
- Managing secure yet functional CORS settings for the frontend-backend interaction

---

## 🌟 Final Note
This project was an incredible learning experience, filled with practical knowledge that goes far beyond classroom concepts. Grateful for every bug, fix, and success!

---

## 📎 Connect with Me!
Let's discuss AI, deployments, and exciting projects 🚀

#AI #MachineLearning #AWS #Deployment #FastAPI #Streamlit #LearningJourney
