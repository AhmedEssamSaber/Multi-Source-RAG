from pypdf import PdfReader


class DocumentLoader:

    def load_pdf(self, path):

        reader = PdfReader(path)
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

        return text

    def load_txt(self, path):

        # UTF-8
        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
                if text.strip():
                    return text
        except:
            pass

        # UTF-16
        try:
            with open(path, "r", encoding="utf-16") as f:
                text = f.read()
                if text.strip():
                    return text
        except:
            pass

        # Latin-1
        try:
            with open(path, "r", encoding="latin-1") as f:
                text = f.read()
                if text.strip():
                    return text
        except:
            pass

        print(f"Failed to read file: {path}")
        return ""
