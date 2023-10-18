import pdfplumber
from pptx import Presentation
from pptx.util import Inches
import nltk
from nltk.corpus import stopwords as nltk_stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx

# Download NLTK stopwords data if not already downloaded
nltk.download("stopwords")


def read_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text


def sentence_similarity(sent1, sent2, stopwords):
    sent1 = [word.lower() for word in sent1]
    sent2 = [word.lower() for word in sent2]

    all_words = list(set(sent1 + sent2))

    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)

    for word in sent1:
        if word not in stopwords:
            vector1[all_words.index(word)] += 1

    for word in sent2:
        if word not in stopwords:
            vector2[all_words.index(word)] += 1

    return 1 - cosine_distance(vector1, vector2)


def build_similarity_matrix(sentences, stopwords):
    similarity_matrix = np.zeros((len(sentences), len(sentences)))

    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i != j:
                similarity_matrix[i][j] = sentence_similarity(
                    sentences[i], sentences[j], stopwords)

    return similarity_matrix


def generate_summary(text, num_sentences=3):
    sentences = nltk.sent_tokenize(text)
    custom_stopwords = set(nltk_stopwords.words("english"))

    similarity_matrix = build_similarity_matrix(sentences, custom_stopwords)

    # Use PageRank algorithm to rank sentences
    sentence_scores = nx.pagerank(nx.from_numpy_array(similarity_matrix))

    # Sort sentences by score in descending order
    ranked_sentences = sorted(((sentence, sentence_scores[i]) for i, sentence in enumerate(
        sentences)), key=lambda x: x[1], reverse=True)

    # Select the top `num_sentences` sentences for the summary
    summary = [sentence for sentence, _ in ranked_sentences[:num_sentences]]
    return "\n".join(summary)


def create_ppt_from_chapter_summaries(pdf_path, output_pptx_path):
    presentation = Presentation()
    chapter_content = []  # Store content for the current chapter
    chapter_title = None

    text = read_pdf(pdf_path)

    for sentence in nltk.sent_tokenize(text):
        if "Chapter" in sentence:
            if chapter_content:
                summary = generate_summary(
                    " ".join(chapter_content), num_sentences=3)
                if summary:
                    create_summary_slide(presentation, chapter_title, summary)

            chapter_content = []
            chapter_title = sentence.strip()
        else:
            chapter_content.append(sentence)

    # Generate a summary for the last chapter and add it to a slide
    if chapter_content:
        summary = generate_summary(" ".join(chapter_content), num_sentences=3)
        if summary:
            create_summary_slide(presentation, chapter_title, summary)

    presentation.save(output_pptx_path)


def create_summary_slide(presentation, title, content):
    slide = presentation.slides.add_slide(
        presentation.slide_layouts[5])  # Blank slide layout
    slide.shapes.title.text = title
    slide.shapes.title.text_frame.paragraphs[0].font.size = Inches(
        0.5)  # Set title font size to 0.5 inch
    text_box = slide.shapes.add_textbox(
        Inches(1), Inches(1.5), Inches(8), Inches(5.5))
    text_frame = text_box.text_frame
    p = text_frame.add_paragraph()
    p.text = content


# Set the path to your PDF file and the output PPTX file
pdf_path = "ML2.pdf"
output_pptx_path = "output.pptx"
create_ppt_from_chapter_summaries(pdf_path, output_pptx_path)
