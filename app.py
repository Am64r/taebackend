from flask import Flask, request, jsonify, send_from_directory
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

from langchain.embeddings.openai import OpenAIEmbeddings

warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)

apikey = os.getenv('APIKEY')

os.environ["OPENAI_API_KEY"] = apikey

app = Flask(__name__)
CORS(app)  # This will handle the CORS issues

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s',
                    handlers=[logging.StreamHandler()])

logger = logging.getLogger(__name__)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/generate-text', methods=['GET'])
def generate_text():
    try:
        data = request.json
        logger.debug(f"Received request data: {data}")

        query = data['text']
        
        logger.debug("Loading Docs")
        loader = DirectoryLoader('data/')

        embeddings = OpenAIEmbeddings()

        index = VectorstoreIndexCreator(embedding=embeddings).from_loaders([loader])

        logger.debug("Querying Index")

        result = index.query(query, llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo",))

        logger.debug(f"Sending response: {result}")

        return jsonify({'generatedText': result})
    
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return "Flask server is running"

@app.route('/hello-world')
def hw():
    return "Hello World"

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    app.run(port=8000) #5000


#deploy on aws lambda