import os
import json
import logging
import azure.functions as func
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from openai import AzureOpenAI

# Load environment variables from .env
load_dotenv()

# Azure Search config
AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
AZURE_SEARCH_INDEX_NAME = os.getenv("AZURE_SEARCH_INDEX_NAME")

# Azure OpenAI config
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
AZURE_OPENAI_API_VERSION = "2024-12-01-preview"

def search_documents(query, top_k=3):
    try:
        logging.info(f"Searching for: {query}")
        search_client = SearchClient(
            endpoint=AZURE_SEARCH_ENDPOINT,
            index_name=AZURE_SEARCH_INDEX_NAME,
            credential=AzureKeyCredential(AZURE_SEARCH_KEY)
        )
        results = search_client.search(
            search_text=query,
            top=top_k
        )
        docs = []
        for result in results:
            question = result.get('question', '')
            documents = result.get('documents', '')
            logging.info(f"Found result - Question: {question} | Documents: {documents}")
            if question and documents:
                docs.append(f"Question: {question}\n\nDocuments:\n{documents}\n\n")
        logging.info(f"Total retrieved docs: {len(docs)}")
        return docs
    except Exception as e:
        logging.error(f"Error in search_documents: {str(e)}")
        return []

def get_openai_answer(user_question, retrieved_docs):
    try:
        client = AzureOpenAI(
            api_version=AZURE_OPENAI_API_VERSION,
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            api_key=AZURE_OPENAI_API_KEY
        )

        system_prompt = (
            "You are a helpful assistant. You give very grounded answers based strictly on the provided context, "
            "with no additional information or speculation. Only use the information from the context below.\n\n"
        )

        prompt = system_prompt
        for idx, doc in enumerate(retrieved_docs):
            prompt += f"Document {idx}:\n{doc}\n"
        prompt += f"\nUser question: {user_question}\n\nAnswer:"

        logging.info(f"Sending prompt to OpenAI: {prompt}")

        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1024,
            temperature=0.3,
            top_p=0.95
        )
        answer = response.choices[0].message.content.strip()
        logging.info(f"OpenAI response: {answer}")
        return answer
    except Exception as e:
        logging.error(f"Error in get_openai_answer: {str(e)}")
        return "An error occurred while generating the answer."

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
        user_question = req_body.get("question")
        logging.info(f"Received question: {user_question}")
        if not user_question:
            return func.HttpResponse(
                json.dumps({"error": "Missing 'question' field"}),
                status_code=400,
                mimetype="application/json"
            )

        retrieved_docs = search_documents(user_question)
        if not retrieved_docs:
            logging.info("No relevant documents found.")
            return func.HttpResponse(
                json.dumps({"answer": "No relevant documents found."}),
                status_code=200,
                mimetype="application/json"
            )

        answer = get_openai_answer(user_question, retrieved_docs)
        return func.HttpResponse(
            json.dumps({"answer": answer}),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        logging.error(f"Unhandled exception in main: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )
