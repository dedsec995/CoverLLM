# utils.py
import ollama
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
import json
import fitz
import re
import unicodedata
from datetime import datetime
current_date = datetime.now()


def extract_text_from_pdf(pdf_file):
    text = ""
    try:
        with fitz.open(stream=pdf_file.read(), filetype="pdf") as pdf_document:
            for page_num in range(pdf_document.page_count):
                page = pdf_document.load_page(page_num)
                text += page.get_text()
        text = unicodedata.normalize("NFKC", text)

        text = re.sub(r"\s+", " ", text)
        text = text.strip()
    except Exception as e:
        print(f"Error: {e}")
    return text


def generate_cover_letter(job_description, company_name, job_title, applicant_info):
    prompt = f"""
    Job Description:
    {job_description}

    Applicant Information:
    {applicant_info}

    Write a small professional cover letter of 3 paragraphs at {company_name} for {job_title}. I just want paragraphs without header or footer.
    """

    response = ollama.chat(
        model="deepseek-r1",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )
    raw_content = response["message"]["content"].strip()
    match = re.search(r"</think>(.*)", raw_content, re.DOTALL)
    cleaned_content = match.group(1).strip() if match else raw_content
    return cleaned_content


def create_cover_letter_pdf(content, job_title, company_name, data):
    name = data["name"]
    email = data["email"]
    website = data["website"]

    # Register Calibri font (adjust path as needed)
    pdfmetrics.registerFont(TTFont("Calibri", "calibri.ttf"))

    # Use A4 with 1-inch (72 pt) margins
    doc = SimpleDocTemplate(
        f"coverLetter/{job_title.replace('/', '-')}-{company_name}.pdf",
        pagesize=A4,
        leftMargin=72,
        rightMargin=72,
        topMargin=72,
        bottomMargin=72,
    )

    styles = getSampleStyleSheet()
    # Custom styles to mimic the LaTeX template
    header_name_style = ParagraphStyle(
        "HeaderName",
        parent=styles["Normal"],
        fontName="Calibri",
        fontSize=24,
        leading=28,
        alignment=TA_LEFT,
        spaceAfter=4,
    )
    header_website_style = ParagraphStyle(
        "HeaderWebsite",
        parent=styles["Normal"],
        fontName="Calibri",
        fontSize=12,
        textColor=colors.gray,
        alignment=TA_LEFT,
        spaceAfter=12,
    )
    date_style = ParagraphStyle(
        "Date",
        parent=styles["Normal"],
        fontName="Calibri",
        fontSize=11,
        leading=14,
        alignment=TA_LEFT,
    )
    address_style = ParagraphStyle(
        "Address",
        parent=styles["Normal"],
        fontName="Calibri",
        fontSize=11,
        leading=14,
        alignment=TA_RIGHT,
    )
    greeting_style = ParagraphStyle(
        "Greeting",
        parent=styles["Normal"],
        fontName="Calibri",
        fontSize=11,
        leading=14,
        alignment=TA_LEFT,
        spaceAfter=12,
    )
    body_style = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontName="Calibri",
        fontSize=11,
        leading=14,
        alignment=TA_LEFT,
        spaceAfter=12,
    )
    closing_style = ParagraphStyle(
        "Closing",
        parent=styles["Normal"],
        fontName="Calibri",
        fontSize=11,
        leading=14,
        alignment=TA_LEFT,
        spaceAfter=2,
    )
    signature_style = ParagraphStyle(
        "Signature",
        parent=styles["Normal"],
        fontName="Calibri",
        fontSize=11,
        leading=14,
        alignment=TA_LEFT,
    )

    story = []

    # Header: Name and Website (mimicking \header{...}{...})
    story.append(Paragraph(f"<b>{name}</b>", header_name_style))
    story.append(Paragraph(website, header_website_style))
    story.append(Spacer(1, 28))  # ~1cm vertical space
    formatted_date = current_date.strftime("%d %b %Y").lstrip("0")
    # Date and Address block (mimicking \dateAndAddress)
    # Left: fixed date ("2 Feb 2025"); Right: address details
    date_text = f"<b>{formatted_date}</b>"
    address_text = (
        data["address"] +
        f"<a href='mailto:{email}'>{email}</a>"
    )
    date_para = Paragraph(date_text, date_style)
    address_para = Paragraph(address_text, address_style)
    # Table with two columns (approximate widths: left=271, right=180)
    table = Table([[date_para, address_para]], colWidths=[271, 180])
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ALIGN", (0, 0), (0, 0), "LEFT"),
                ("ALIGN", (1, 0), (1, 0), "RIGHT"),
                ("LINEBELOW", (0, 0), (-1, 0), 0, colors.white),
            ]
        )
    )
    story.append(table)
    story.append(Spacer(1, 24))

    # Opening Greeting
    story.append(Paragraph("<b>Dear Hiring Manager,</b>", greeting_style))

    # Body: Split the provided content into paragraphs
    for para in content.strip().split("\n\n"):
        if para.strip():
            story.append(Paragraph(para.strip(), body_style))

    story.append(Spacer(1, 28))
    # Closing and signature (mimicking the LaTeX closing)
    story.append(Paragraph("Best regards,", closing_style))
    story.append(Paragraph(f"<b>{name}</b>", signature_style))

    doc.build(story)
