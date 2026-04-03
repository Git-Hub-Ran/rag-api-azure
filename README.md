# 🐾 Weird Animals RAG API (Azure + OpenAI)

## 📌 Description

This project implements a Retrieval-Augmented Generation (RAG) system that answers questions about unusual animals.

It retrieves relevant document chunks using semantic search and generates grounded answers using Azure OpenAI.

The system ensures that answers are based only on the provided data and avoids hallucinations.

---

## 🧠 Architecture

User → HTTP Request → Azure Function → Vector Search → LLM → JSON Response

The system uses lazy initialization to avoid repeated heavy processing and improve performance.

---

## 📂 Project Structure

- `shared_rag.py`  
  Contains the core RAG logic:
  - Loads documents from Azure Blob Storage  
  - Splits them into chunks  
  - Creates embeddings using Azure OpenAI  
  - Stores vectors in Chroma  
  - Implements the `ask_question` function  

- `function_app.py`  
  Defines the HTTP API using Azure Functions.  
  Receives a question and returns an answer with sources.

- `requirements.txt`  
  Lists all dependencies required to run the project.

- `host.json`  
  Configuration file for Azure Functions runtime.

---

## 🚀 API Usage

### Endpoint

POST /api/ask

### Request

```json
{
  "question": "Which animal can regenerate body parts?"
}
```

### Response

```json
{
  "answer": "Based on the provided information...",
  "sources": ["axolotl.md"]
}
```

---

## 🧠 Guardrails Example

```json
{
  "question": "Where is Amsterdam?"
}
```

Response:

```json
{
  "answer": "I don't know.",
  "sources": []
}
```

---

## 📸 Screenshots

### ✅ Successful API Response
![Success](images/Hoppscotch_with_answer_that_work.png)

### ❓ Unknown Question (Guardrail)
![Unknown](images/Hoppscotch_with_answer_that_does_not_work.png)

### 🚀 Deployment Success
![Deployment](images/Deployment_Center_succeeded.png)

### 📂 GitHub Repository
![Repo](images/repo_github.png)

---

## ⚙️ Tech Stack

- Azure Functions (Python)  
- Azure Blob Storage  
- Azure OpenAI  
- LangChain  
- ChromaDB  
- GitHub Actions  

---

## 🛠️ Deployment

- Code pushed to Dev branch  
- GitHub Actions builds and deploys automatically  
- Azure Functions (Flex Consumption plan)  

---

## ⚠️ Notes

- The system only answers based on retrieved documents  
- If the answer is not found in the data, it returns: "I don't know"  

---

## 🎯 Purpose

This project demonstrates:
- Retrieval-Augmented Generation (RAG)  
- Semantic search using vector databases  
- Integration between Azure services and LLMs  
- Building a production-style AI API  

---

## 👨‍💻 Author

Ran
