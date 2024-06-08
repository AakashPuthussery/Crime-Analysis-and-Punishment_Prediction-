from flask import Flask, request, render_template

app = Flask(__name__)

# Include the functions from previous steps
import fitz  # PyMuPDF
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests

# Function to extract PDF text
def extract_pdf_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

# Function to structure the extracted text
def structure_text(text):
    sections = re.split(r'(\d+\.\s)', text)
    penal_code = {}
    current_key = None
    for section in sections:
        if re.match(r'\d+\.\s', section):
            current_key = section.strip()
            penal_code[current_key] = ""
        elif current_key:
            penal_code[current_key] += section.strip()
    return penal_code

# Function to find the closest section
def find_closest_section(user_input, penal_code):
    corpus = [user_input] + list(penal_code.values())
    vectorizer = TfidfVectorizer().fit_transform(corpus)
    vectors = vectorizer.toarray()
    cosine_matrix = cosine_similarity(vectors)
    similarity_scores = cosine_matrix[0][1:]
    closest_index = similarity_scores.argmax()
    closest_section = list(penal_code.keys())[closest_index]
    return closest_section, penal_code[closest_section]

# Function to fetch news articles
def fetch_news(query, api_key):
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json().get('articles', [])
        return articles
    else:
        return []

# Load and structure the penal code data
pdf_path = "/workspaces/Crime-Detection-and-Punishment_Prediction-Chat-Bot/Doc/IPC.pdf"
pdf_text = extract_pdf_text(pdf_path)
penal_code = structure_text(pdf_text)
api_key = "9d9b514c72b440a0b72bf641a2a32a71"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['crime_description']
        closest_section, section_text = find_closest_section(user_input, penal_code)
        news_articles = fetch_news(user_input, api_key)
        return render_template('results.html', 
                               closest_section=closest_section, 
                               section_text=section_text, 
                               news_articles=news_articles)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5002, debug=True)
