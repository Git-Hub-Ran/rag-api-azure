#=================================================
#Connect to Azure Blob Storage and load documents:
#=================================================

# Import the Azure Blob client so we can connect to Blob Storage
from azure.storage.blob import BlobServiceClient
import os

# Read the connection string from the environment variable
connection_string = os.environ["AZURE_STORAGE_CONNECTION_STRING"]

# Set the container name
container_name = "weird-animal-docs"

# Create the storage client and container client
blob_service_client = BlobServiceClient.from_connection_string(connection_string) #connect to Azure Storage
container_client = blob_service_client.get_container_client(container_name) #Go to the container with my files

# Load all documents from the container
documents = []

for blob in container_client.list_blobs():
    blob_client = container_client.get_blob_client(blob)
    content = blob_client.download_blob().readall().decode("utf-8")

    documents.append({
        "name": blob.name,
        "content": content
    })

# Print a simple check
print(f"Loaded {len(documents)} documents")
print("First document:", documents[0]["name"])

#=================================================
#Split the documents into chunks:
#=================================================
# Import the text splitter used to break long documents into smaller chunks
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Create a splitter that divides text into chunks with small overlap
splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,   # each chunk will be about 400 characters
    chunk_overlap=50  # keep a small overlap to preserve context
)

# Create empty lists to store chunk text and metadata
texts = []
metadatas = []

# Loop through all loaded documents
for doc in documents:
    # Split the document content into smaller chunks
    chunks = splitter.split_text(doc["content"])

    # Save each chunk and remember which file it came from
    for chunk in chunks:
        texts.append(chunk)
        metadatas.append({"source": doc["name"]})

# Print how many chunks were created
print("Chunks:", len(texts))

# Print one sample chunk to inspect the output
print(texts[0])

#=================================================
#Connect to Azure OpenAI embedding deployment:
#=================================================
# Import the Azure embeddings class from LangChain
from langchain_openai import AzureOpenAIEmbeddings

# Create embeddings object using my Azure OpenAI resource
embeddings = AzureOpenAIEmbeddings(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],  # my Azure endpoint
    api_key=os.environ["AZURE_OPENAI_API_KEY"],          # my API key
    deployment="text-embedding-3-small-model"            # my deployment name
)

# Test embedding on a simple sentence
vector = embeddings.embed_query("This is a weird animal")

# Print vector length to confirm it works
print("Vector size:", len(vector))

#=================================================
#Create Vector store DB:
#=================================================
# Import Chroma, a vector database for semantic search
from langchain_chroma import Chroma

# Build a vector store from the chunked texts and their embeddings
vectorstore = Chroma.from_texts(
    texts,                 # all text chunks
    embedding=embeddings,  # embedding model
    metadatas=metadatas    # source information for each chunk
)

# Confirm that the vector database was created
print("Vector DB created successfully")

#======================================================
#Connect to Azure OpenAI chat model and test response:
#======================================================
# Import the Azure chat model class from LangChain
from langchain_openai import AzureChatOpenAI

# Create the chat model client using my Azure OpenAI deployment
llm = AzureChatOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],  # Azure OpenAI endpoint
    api_key=os.environ["AZURE_OPENAI_API_KEY"],          # Azure OpenAI API key
    api_version="2024-10-21",                            # Azure OpenAI API version used by this client
    deployment_name="gpt-4.1-nano-model",                # My chat deployment name in Azure AI Foundry
    temperature=0                                        # Keep answers stable and deterministic
)

# Test the model with a simple message
response = llm.invoke("Say hello in one short sentence.")

# Print the model response
print(response.content)

#======================================================
#RAG Function:
#======================================================
# Define a function that answers questions using Retrieval-Augmented Generation (RAG)
def ask_question(query):

    # Step 1: retrieve relevant chunks using vector similarity
    docs = vectorstore.similarity_search(query, k=3)

    # Step 2: combine retrieved chunks into one context string
    context = "\n\n".join([d.page_content for d in docs])

    # Step 3: guardrail - if no context found
    if not context.strip():
      return {"answer": "I don't know.", "sources": []}

    # Step 4: create a prompt that forces the model to use only the retrieved context
    prompt = f"""
    You are a careful research assistant.
    You answer in a very polite way.

    Rules:
    - Answer only using the context below
    - If the answer is not in the context, say "I don't know."
    - Do NOT make up information

    Context:
    {context}

    Question:
    {query}
    """

    # Step 5: send prompt to the chat model and get response
    response = llm.invoke(prompt)

        # clean the model answer:
    answer = response.content.strip()

    # if the model says it does not know, do not return sources:
    if answer.lower() == "i don't know." or answer.lower() == "i don't know":
        return {"answer": "I don't know.", "sources": []}

    # Step 7: remove duplicate sources while keeping the order:
    unique_sources = []
    for d in docs:
        source = d.metadata["source"]
        if source not in unique_sources:
            unique_sources.append(source)

    # Step 8: return sources:
    return {"answer": answer, "sources": unique_sources}
