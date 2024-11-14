from dotenv import load_dotenv
import base64
import streamlit as st
import os
import io
import requests
from PIL import Image 
import pdf2image
import google.generativeai as genai
from google.cloud import language_v1

# Set up environment variables and API keys
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '/path/to/your/ATS.json'
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get Gemini response
def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

# Function to setup PDF file
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        pdf_parts = [{"mime_type": "image/jpeg", "data": base64.b64encode(img_byte_arr).decode()}]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Custom CSS for styling
st.markdown(
    """
    <style>
    /* Custom styling */
    body {
        background-color: #f5f7fa;
        font-family: 'Arial', sans-serif;
    }
    .header {
        padding: 20px;
        text-align: center;
        background: #0078d7;
        color: white;
        font-size: 2.5em;
    }
    .container {
        max-width: 800px;
        margin: auto;
        padding: 20px;
    }
    .section-title {
        font-size: 1.8em;
        margin-bottom: 10px;
        color: #333;
    }
    .description {
        color: #6c757d;
        font-size: 1.1em;
        text-align: center;
    }
    .sidebar .sidebar-content {
        background-color: #343a40;
        color: white;
    }
    .button {
        background-color: #0078d7;
        color: white;
        font-size: 1.2em;
        border-radius: 8px;
        padding: 8px 20px;
    }
    .button:hover {
        background-color: #0056b3;
    }
    .footer {
        padding: 20px;
        text-align: center;
        font-size: 0.9em;
        color: #6c757d;
        background-color: #f1f3f5;
    }
    </style>
    """, unsafe_allow_html=True
)

# Page Configuration
st.set_page_config(page_title="ATS Resume Expert", layout="wide")

# Header Section
st.markdown("<div class='header'>ATS Resume Optimization Tool</div>", unsafe_allow_html=True)
st.markdown("<p class='description'>Optimize your resume for Applicant Tracking Systems (ATS) to increase your job application success rate.</p>", unsafe_allow_html=True)

# Main Container
st.markdown("<div class='container'>", unsafe_allow_html=True)

# Sidebar for actions
st.sidebar.title("Options")
action = st.sidebar.radio("Choose an Action", [
    "Tell Me About the Resume",
    "How Can I Improve my Skills",
    "Percentage Match",
    "Recommendations to Improve ATS Score",
    "Modify into Measurable Achievements",
    "Keyword Recommendations",
    "Rewrite Resume to Suit Job Description",
    "Generate Cover Letter"
])

# Job Description Input
st.markdown("<div class='section-title'>Enter Job Description</div>", unsafe_allow_html=True)
input_text = st.text_area("Paste the job description here:", key="input", height=150)

# File uploader for resume PDF
st.markdown("<div class='section-title'>Upload Your Resume (PDF)</div>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Select your resume file (PDF format only)", type=["pdf"])

# Button to process resume and job description
submit_button = st.button("Process Resume", key="process_button", help="Click to analyze your resume")

if uploaded_file is not None:
    st.success("PDF uploaded successfully!")
    pdf_content = input_pdf_setup(uploaded_file)

    if submit_button:
        if action == "Tell Me About the Resume":
            prompt = """
            You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description.
            Please share your professional evaluation on whether the candidate's profile aligns with the role.
            Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
            """
            response = get_gemini_response(input_text, pdf_content, prompt)
            st.subheader("Evaluation of Your Resume:")
            st.write(response)

        elif action == "How Can I Improve my Skills":
            prompt = """
            You are an HR consultant with technical knowledge across multiple domains...
            """
            response = get_gemini_response(input_text, pdf_content, prompt)
            st.subheader("Skill Improvement Suggestions:")
            st.write(response)

        # Additional actions continue here...

else:
    st.warning("Please upload a resume and provide a job description to proceed.")

st.markdown("</div>", unsafe_allow_html=True)  # Close the main container

# Footer Section
st.markdown("<div class='footer'>© 2024 ATS Resume Optimization. All rights reserved.</div>", unsafe_allow_html=True)
