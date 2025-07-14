from PyPDF2 import PdfReader

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_image(file_path):
    from PIL import Image
    import pytesseract
    image = Image.open(file_path)
    text = pytesseract.image_to_string(image, lang='eng')
    return text
