# app.py
import streamlit as st
import json
import streamlit.components.v1 as com
from utils import extract_text_from_pdf, generate_cover_letter, create_cover_letter_pdf
import os, time

json_file = "details.json"
os.makedirs("coverLetter",exist_ok=True)

# Check if details.json exists
if not os.path.exists(json_file):
    st.info("First time setup: Please enter your details.")
    name = st.text_input("Enter your name:")
    email = st.text_input("Enter your email:")
    website = st.text_input("Enter your portfolio website:")
    if st.button("Save Details"):
        if name and email and website:
            data = {"name": name, "email": email, "website": website, "content": ""}
            with open(json_file, "w") as file:
                json.dump(data, file, indent=4)
            st.success("Details saved! Redirecting.....")
            st.rerun()
        else:
            st.error("Please fill in all fields.")
    st.stop()

# Load existing data
with open(json_file, "r") as file:
    data = json.load(file)

col1, col2 = st.columns([8,7])
with col1:
    st.title("Cover Letter Generator")
with col2:
    com.iframe("https://lottie.host/embed/5f753811-3ae0-45a4-98a0-89530560eb7d/dfld3ulPRd.lottie", height=100)
    
company_name = st.text_input("Enter the company name:")
job_title = st.text_input("Enter the job title:")
job_description = st.text_area("Enter the job description:")

if st.checkbox("Upload a new resume (Optional)") or not data.get("content"):
    uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")
    if uploaded_file is not None:
        resume_text = extract_text_from_pdf(uploaded_file)
        data["content"] = resume_text
        with open(json_file, "w") as file:
            json.dump(data, file, indent=4)
        st.success("Resume uploaded and saved!")
else:
    st.info("Resume information found in details.json.")

if "cover_letter" not in st.session_state:
    st.session_state.cover_letter = ""

if st.button("Generate Cover Letter"):
    if company_name and job_title and job_description:
        if data.get("content"):
            with com.iframe("https://lottie.host/embed/340142c6-d731-49c1-9342-a9f69626b3e9/qFKZwJuPOV.lottie"):
                st.session_state.cover_letter = generate_cover_letter(job_description, company_name, job_title, data["content"])
            st.success("Cover letter generated! You can now edit it below.")
        else:
            st.error("Please upload a resume or add content to details.json.")
    else:
        st.error("Please provide company name, job title, and job description.")

if st.session_state.cover_letter:
    edited_cover_letter = st.text_area(
        "Edit your cover letter:", value=st.session_state.cover_letter, height=300
    )

    if st.button("Create PDF"):
        with com.iframe("https://lottie.host/embed/0d0a0589-b6c1-41a8-a690-08a0f70f753c/OMqTFrrEAY.lottie"):
            try:
                time.sleep(10)
                create_cover_letter_pdf(edited_cover_letter, job_title, company_name, data)
                st.success("Cover letter PDF created successfully!")

                with open(
                    f"coverLetter/{job_title.replace('/', '-')}-{company_name}.pdf",
                    "rb",
                ) as file:
                    st.download_button(
                        label="Download Cover Letter",
                        data=file,
                        file_name=f"cover_letter_{company_name}_{job_title}.pdf",
                        mime="application/pdf",
                    )
            except Exception as e:
                st.error(f"Error generating PDF: {e}")

# https://lottie.host/embed/340142c6-d731-49c1-9342-a9f69626b3e9/qFKZwJuPOV.lottie
# https://lottie.host/embed/0d0a0589-b6c1-41a8-a690-08a0f70f753c/OMqTFrrEAY.lottie
# https://lottie.host/embed/5f753811-3ae0-45a4-98a0-89530560eb7d/dfld3ulPRd.lottie
