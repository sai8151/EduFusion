import spacy
import pytextrank
import random
import pdfplumber
import os
from pptx import Presentation
from pptx.util import Inches

text=""
script_directory = os.path.dirname(os.path.realpath(__file__))
pdf_path = os.path.join(script_directory, 'ML2.pdf')
nlp = spacy.load("en_core_web_lg")
nlp.add_pipe("textrank")

def getPoint(text):
   doc = nlp(text)
   print("\n\noutput:\n\n")
   for sent in doc._.textrank.summary(limit_phrases=random.randint(0, 30), limit_sentences=random.randint(3, 5)):
    print("Summary Sentence:")
    print(sent)

with pdfplumber.open(pdf_path) as pdf:
    for page_num in range(len(pdf.pages)):
        page = pdf.pages[page_num]
        text = page.extract_text()
        if text:  # Check if the page is not empty
            getPoint(text)

print("Extracted Text:")
print(text)

getPoint(text)