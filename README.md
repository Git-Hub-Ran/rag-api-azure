# Weird Animals RAG Chatbot (Azure + OpenAI)

## 📌 Description

This project implements a Retrieval-Augmented Generation (RAG) system that answers questions about unusual animals.

It retrieves relevant document chunks using semantic search and generates grounded answers using Azure OpenAI.

The system ensures that answers are based only on the provided data and does not hallucinate information.

------------------------------------------------------------------------

## 🧠 Architecture

User → HTTP Request → Azure Function → Vector Search → LLM → JSON
Response

------------------------------------------------------------------------

## 📂 Project Structure

-   `shared_rag.py`\
    Contains the core RAG logic:

    -   Loads documents from Azure Blob Storage\
    -   Splits them into chunks\
    -   Creates embeddings using Azure OpenAI\
    -   Stores vectors in Chroma\
    -   Implements the `ask_question` function

-   `function_app.py`\
    Defines the HTTP API using Azure Functions.\
    Receives a question and returns an answer with sources.

-   `requirements.txt`\
    Lists all dependencies required to run the project.

-   `host.json`\
    Configuration file for Azure Functions runtime.

------------------------------------------------------------------------

## 🚀 Example Request

``` json
POST /api/ask
{
  "question": "Which animal can regenerate body parts?"
}
```

------------------------------------------------------------------------

## ✅ Example Response

``` json
{
  "answer": "The axolotl can regenerate body parts.",
  "sources": ["axolotl.md"]
}
```

------------------------------------------------------------------------

## 🛠️ Tech Stack

-   Azure Functions\
-   Azure Blob Storage\
-   Azure OpenAI\
-   LangChain\
-   Chroma (Vector Database)

------------------------------------------------------------------------

## ⚠️ Notes

-   The system only answers based on retrieved documents.
-   If the answer is not found in the data, it returns: I don't know.

------------------------------------------------------------------------

## 🎯 Purpose

This project demonstrates: - Retrieval-Augmented Generation (RAG) -
Semantic search using vector databases - Integration between Azure
services and LLMs - Building a production-style API for AI applications
