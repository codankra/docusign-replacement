# Do you just need to sign your own PDF file?

This Python script overlays a **handwriting-style signature** and **human-friendly date** at the bottom of the **last page** of a PDF.

---

## Installation

```bash
# Clone repository
git clone https://github.com/codankra/docusign-replacement.git
cd docusign-replacement

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

# Install dependencies
pip install reportlab PyPDF2 requests
```

---

## Usage

Place your PDF in the repository folder and name it `input.pdf`, or update the script with your desired file path.

```bash
python sign_pdf.py
```

The signed PDF will be saved as `signed.pdf` in the same folder.

---

## Customization

Edit the following values in `sign_pdf.py`:

- **Signature name:** change the `SIGNATURE_NAME` variable.
- **Date format:** adjust the `strftime` string for `today_str`.
- **Font size:** change the number in `c.setFont(FONT_NAME, 16)`.
- **Placement:** adjust the `y_pos` variable.
