
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter
import io
import datetime
import os
import requests
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FONT_NAME = "Handwriting"
FONT_FILE = "DancingScript-Regular.ttf"
FONT_URL = "https://raw.githubusercontent.com/google/fonts/main/ofl/dancingscript/DancingScript-Regular.ttf"

# Download if missing
if not os.path.exists(FONT_FILE):
    print("Downloading handwriting font...")
    r = requests.get(FONT_URL)
    with open(FONT_FILE, "wb") as f:
        f.write(r.content)

# Register font
pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_FILE))



# File paths
input_pdf = "input.pdf"   # your original PDF
output_pdf = "signed.pdf" # output file

# Read original PDF
existing_pdf = PdfReader(open(input_pdf, "rb"))
last_page = existing_pdf.pages[-1]
page_width = float(last_page.mediabox.width)
page_height = float(last_page.mediabox.height)

# Create overlay PDF in memory (same size as last page)
packet = io.BytesIO()
c = canvas.Canvas(packet, pagesize=(page_width, page_height))

margin = 50
y_pos = 50  # Distance from bottom

# --- Signature line (left) ---
c.line(margin, y_pos, margin + 200, y_pos)
c.setFont("Helvetica", 10)
c.drawString(margin, y_pos - 12, "Signature")

# --- Date line (right) ---
date_line_start = page_width - margin - 150
c.line(date_line_start, y_pos, page_width - margin, y_pos)

# Label for date (smaller, normal)
c.setFont("Helvetica", 10)
c.drawString(date_line_start, y_pos - 12, "Date")

# Signature in italic Courier (built-in "pseudo handwriting")
c.setFont(FONT_NAME, 16)
c.drawString(margin + 5, y_pos + 5, "Daniel Kramer")

# Date in bold Helvetica
c.setFont("Helvetica-Bold", 10)
today_str = datetime.date.today().strftime("%B %d, %Y")
c.drawString(date_line_start + 5, y_pos + 5, today_str)

c.save()
packet.seek(0)

# Merge overlay onto last page
overlay_pdf = PdfReader(packet)
output = PdfWriter()
for i, page in enumerate(existing_pdf.pages):
    if i == len(existing_pdf.pages) - 1:
        page.merge_page(overlay_pdf.pages[0])
    output.add_page(page)

# Save final PDF
with open(output_pdf, "wb") as f:
    output.write(f)

print(f"Saved signed PDF as: {output_pdf}")
