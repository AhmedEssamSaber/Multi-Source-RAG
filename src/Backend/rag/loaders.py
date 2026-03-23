from pypdf import PdfReader

def load_pdf(path):

    reader = PdfReader(path)
    text = ""
    
    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text
    
    return text

def load_txt(path):

    with open(path, "r", encoding="utf-8") as f:
        text = f.read()