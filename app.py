from flask import Flask, request, render_template, jsonify
import PyPDF2

app = Flask(__name__)

class PDFChatBot:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.text = self.extract_text_from_pdf()

    def extract_text_from_pdf(self):
        text = ""
        with open(self.pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
        return text

    def answer_question(self, question):
        if question.lower() in self.text.lower():
            return f"I found something about '{question}':\n{self.find_relevant_paragraph(question)}"
        else:
            return "I couldn't find anything related to your question."

    def find_relevant_paragraph(self, keyword):
        paragraphs = self.text.split('\n\n')
        for paragraph in paragraphs:
            if keyword.lower() in paragraph.lower():
                return paragraph
        return "No relevant information found."

# Initialize the chatbot with your PDF file
chatbot = PDFChatBot("F:\Crime-Detection-and-Punishment_Prediction-Chat-Bot\IPC.pdf")  # Replace with your PDF file path

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data['question']
    answer = chatbot.answer_question(question)
    return jsonify({'answer': answer})

if __name__ == "__main__":
    app.run(debug=True)
