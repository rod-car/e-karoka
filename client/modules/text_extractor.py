import re
import os
import fitz
import json
from docx import Document
from odf import text as odf_text
from odf import teletype
import win32com.client

def guess_file_type(path: str) -> str:
    _, file_extension = os.path.splitext(path.lower())
    file_type_mapping = {".pdf": "pdf", ".docx": "docx", ".odt": "odt", ".doc": "doc"}
    return file_type_mapping.get(file_extension, "unknown")

def extract_text(path: str) -> str:
    file_type = guess_file_type(path)
    text = ""

    if file_type == "pdf":
        with fitz.open(path) as doc:
            num_pages = doc.page_count
            for page_num in range(num_pages):
                page = doc.load_page(page_num)
                text += page.get_text()
                
    elif file_type == "docx":
        doc = Document(path)
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
            
    elif file_type == "odt":
        odt_doc = odf_text.load(path)
        text = teletype.extractText(odt_doc)
        
    elif file_type == "doc":
        word_app = win32com.client.Dispatch("Word.Application")
        doc = word_app.Documents.Open(path)
        text = doc.Range().Text
        doc.Close()
        word_app.Quit()
        
    elif file_type == "unknown":
        try:
            with open(path, "r", encoding="utf-8") as file:
                text = file.read()
        except Exception as e:
            print(f"Error reading file: {e}")

    return text

def extract_abstract(file):
    abstract = None

    with fitz.open(file) as doc:
        num_pages = doc.page_count
        for page_num in range(num_pages):
            page = doc.load_page(page_num)
            text = page.get_text()

            match = re.search(r"(?i)(\n|^)(Abstract|Résumé|Résumé/Abstract|Résumé ou Abstract)", text)

            if match:
                print("Passed here: " + str(match))
                start_pos = match.end()
                remaining_text = text[start_pos:].strip()

                print("Start match: " + str(start_pos))

                # Assuming the abstract section ends with the next major section or heading
                end_match = re.search(
                    r"(?i)(\n|^)(Introduction|Chapitre|Chapter|Conclusion|References|Bibliographie|BIBLIOGRAPHY)", remaining_text)

                if end_match:
                    end_pos = end_match.start()
                    abstract = remaining_text[:end_pos].strip()
                else:
                    abstract = remaining_text.strip()

                break  # Exit the loop once the abstract is found
    return abstract

def extract_author(text):
    author_name = None
    candidate_labels = [
        "Author:", "By:", "Submitted by:", "Thesis presented by:", "Author(s):", "Candidate:",
        "Auteur:", "Par:", "Par", "Soumis par:", "Thèse présentée par:", "Auteur(s):", "Candidat:"
    ]

    for label in candidate_labels:
        match = re.search(rf"(?<={re.escape(label)})(.*)(?=\n)", text, re.IGNORECASE)
        if match:
            author_name = match.group().strip()
            break

    if author_name == None:
        return "N/A"
    return author_name

def extract_title(text: str):
    title_match = re.search(r"\n(.)", text)
    title = None
    return title_match

    if title_match:
        title = title_match.group().strip()
    return title

def extract_bibliographics(file):
    bibliographic_data = []

    with fitz.open(file) as doc:
        num_pages = doc.page_count
        for page_num in range(num_pages):
            page = doc.load_page(page_num)
            text = page.get_text()

            regex = r"\[([^[\]]+)\]\((http[s]?://[^)]+)\)"
            matches = re.findall(regex, text)

            for match in matches:
                author_name = match[0].strip()
                link = match[1].strip()

                bibliographic_data.append(
                    {"author": author_name, "link": link})

    return bibliographic_data

def parse_json_file(file_path) -> dict:
    with open(file_path, 'r', encoding='utf-8') as file:
        documents = dict(json.loads(file.read())[0])
        return documents.items()