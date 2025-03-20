import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import re

# Load environment variables
load_dotenv()
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

# Initialize LLM model
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.0)
output_parser = StrOutputParser()

def generate_career_report(user_details, prompt_template):
    """As per name Function will Generates a career guidance report using the LLM model."""
    chain = prompt_template | llm | output_parser
    return chain.invoke({"user_details": user_details})

def generate_pdf(content):
    """
    Funtion will Generates a PDF from the given content.
    It also designed in such a way to make pdf in stgructured manner.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(name="TitleStyle", fontSize=16, alignment=TA_CENTER, spaceAfter=12, textColor=colors.darkblue, bold=True)
    section_style = ParagraphStyle(name="SectionStyle", fontSize=14, spaceAfter=8, bold=True)
    body_style = ParagraphStyle(name="BodyStyle", fontSize=12, spaceAfter=6, alignment=TA_LEFT)
    bullet_style = ParagraphStyle(name="BulletStyle", fontSize=12, spaceAfter=6, leftIndent=20, bulletIndent=10)

    elements = []
    elements.append(Paragraph("Career Guidance Roadmap", title_style))
    elements.append(Spacer(1, 12))

    for line in content.split("\n"):
        line = line.strip()
        if not line:
            continue
        
        if line.startswith("##"):
            clean_line = line.replace("##", "").strip()
            elements.append(Paragraph(clean_line, section_style))
        elif line.startswith("-"):
            clean_line = line.replace("-", "").strip()
            elements.append(ListFlowable([ListItem(Paragraph(clean_line, bullet_style))]))
        elif re.match(r'\d+\.', line):  # Handle numbered lists
            elements.append(Paragraph(line, bullet_style))
        else:
            elements.append(Paragraph(line, body_style))
        elements.append(Spacer(1, 6))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer
