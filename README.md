# Azure RAG Chatbot – Document Question Answering

**A Retrieval-Augmented Generation (RAG) chatbot for answering queries using a pre-selected document collection, built with Azure AI Search and OpenAI LLMs.**

---

## 🚀 Overview

This project demonstrates how to build a production-grade chatbot that answers questions using a controlled set of documents—**not just generic internet knowledge**.

* **Fixed Dataset:** Users cannot upload arbitrary documents. For demonstration and practice, a Hugging Face (HF) dataset prepared for RAG was uploaded to Azure Blob Storage and indexed.
* **Embedding & Indexing:** Text chunks from these documents are embedded using OpenAI models and indexed with **Azure Cognitive Search**.
* **Semantic Retrieval:** On a user query, the system retrieves top-matching document passages using vector similarity.
* **LLM Answering:** Retrieved passages + user query are passed to GPT-4 (Azure OpenAI), which generates a **grounded, context-aware answer**.
* **Transparency:** Returns the final answer along with references to the underlying documents.

---

## 🌐 Live Demo

Try it here: [https://magenta-ganache-de2bab.netlify.app/](https://magenta-ganache-de2bab.netlify.app/)

---

## 🧠 How It Works (High Level)

1. **Ingestion:**
   A fixed set of documents (from a Hugging Face dataset) was uploaded to Azure Blob Storage.

2. **Processing:**

   * Text is split into manageable “chunks.”

3. **Embedding & Indexing:**

   * Each chunk is embedded into a vector using OpenAI embeddings (text-embedding-ada-002).
   * All vectors are indexed using **Azure Cognitive Search**.

4. **Question Answering:**

   * User asks a question through the chatbot UI or API.
   * The system retrieves the top-k most relevant chunks via vector similarity.
   * Query + context chunks are sent to Azure OpenAI’s GPT-4 with a custom prompt.
   * LLM generates a well-grounded answer, minimizing hallucinations.
   * The chatbot displays the answer **plus links/citations** to the source chunks.

---

## 🛠️ Technologies Used

* **Azure OpenAI (GPT-4, Embeddings)**
* **Azure Cognitive Search**
* **Python, FastAPI (API)**
* **Streamlit or React (for demo UI)**
* **Azure Blob Storage**
* **Prompt Engineering & NLP**

---

## ⚡ Example Usage

> **User:** “What is the company policy on remote work?”
> **Chatbot:**
> *Based on sample\_document.txt, chunk 3:*
> “The company allows up to two days per week of remote work, subject to manager approval. Full-time remote work is not standard except for certain roles.”

---

## 🔐 **Security Note**

* All keys/secrets must be provided in a **local `.env` file** (never committed!).
* For production, use **Azure Key Vault** and managed identities.

---

## ❓ FAQ

**Q: Can users upload their own documents?**
A: **No.** Currently, the system is designed for research and demo purposes only. Only documents included in the demo dataset (uploaded in advance) are available for question answering.

**Q: Can I run this without Azure/OpenAI keys?**
A: The code is designed for Azure, but can be adapted for open-source LLMs and local vector DBs. Sample data pipelines are included for illustration, but end-to-end Q\&A requires cloud credentials.

**Q: What’s unique here?**
A: True “retrieval-augmented” LLM: the chatbot answers ONLY with facts found in your controlled document collection. No more “hallucinated” responses.
Modular—swap out the embedding model or retriever as needed.

---
