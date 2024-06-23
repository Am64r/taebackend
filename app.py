from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
load_dotenv()
import warnings
import logging
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain_core._api.deprecation import LangChainDeprecationWarning
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_core.messages import HumanMessage, SystemMessage
from flask_cors import CORS

warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)

apikey = os.getenv('APIKEY')

os.environ["OPENAI_API_KEY"] = apikey

app = Flask(__name__)
CORS(app)  # This will handle the CORS issues

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/generate-text', methods=['POST'])
def generate_text():
    data = request.json
    logging.debug(f"Received request data: {data}")

    query = data['text']

    loader = TextLoader("data/reference.txt") #could pass a generic url amr,com
    loader2 = DirectoryLoader('data/')

    index = VectorstoreIndexCreator().from_loaders([loader2])

    result = index.query(query, llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo",))

    logging.debug(f"Sending response: {result}")

    return jsonify({'generatedText': result})

@app.route('/')
def index():
    return "Flask server is running"

if __name__ == '__main__':
    app.run(port=8000) #5000


#deploy on aws lambda