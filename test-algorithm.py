from django.core.files.move import file_move_safe
import os

i = os.system("cp doc.pdf new.pdf")
print(i)
# file_move_safe("doc.pdf", "copy.pdf")

print("Moved")
exit(0)

# def get_h(content, terms) -> str:
#         """Recuperer le contenu highlité
# 
#         Args:
#             width (int, optional): _description_. Defaults to 3.
# 
#         Returns:
#             str: _description_
#         """
#         sentences = content.split('.')
# 
#         highlighted_sentences = []
# 
#         for sentence in sentences:
#             for term in terms:
#                 if term in sentence:
#                     if sentence.strip() not in highlighted_sentences:
#                         highlighted_sentences.append("<p>" + sentence.strip() + "</p>")
# 
#         content = " ".join(highlighted_sentences)
#         for term in terms:
#             content = content.replace(term, "<span class='highlighted'>" + str(term) + "</span>")
#         
#         print(content)
#         html_output = " ".join(highlighted_sentences)
#         return html_output
# 
# get_h("Je m'appelle toto. Je suis un test de text", ['Je', 'toto', 'text'])
# exit(0)
# 
# import datetime
# date_str = "01/01/2023"
# date_str = date_str.split("/")
# print(datetime.date(int(date_str[2]), int(date_str[1]), int(date_str[0])))
# exit(0)

import fitz
# from PIL import Image
# import pytesseract
# 
# path = "doc.pdf"
# pdf_image = Image.open(path)
# 
# text = pytesseract.image_to_string(pdf_image)
# print(text)

def extract_text(path: str, file_type = "pdf") -> str:
    text = ""
    if (file_type == "pdf"):
        with fitz.open(path) as doc:
            page = doc[2]
            print(page.get_images())
            
            # num_pages = doc.page_count
            # for page_num in range(num_pages):
            #     page = doc.load_page(page_num)
            #     print(doc.get_page_pixmap(page_num))
            #     text += page.get_text()
            #     print("Page: " + str(page_num))
    else:
        text = ""
        
    return text

print(extract_text("doc.pdf"))