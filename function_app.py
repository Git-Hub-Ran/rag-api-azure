# Import Azure Functions library
import azure.functions as func

# Import json so we can return JSON responses
import json

# Import the RAG function from the shared_rag logic file
from shared_rag import ask_question

# Create the Azure Function App object ( it will be the container that contain all of my functions)
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Define an HTTP route for asking questions
@app.function_name(name="AskQuestion") #AskQuestion is the function name in Azure
@app.route(route="ask") # äsk" is the last part of the URL
def ask_question_api(req: func.HttpRequest) -> func.HttpResponse:
    # Try to read the incoming request body as JSON
    try:
        request_json = req.get_json()
    except ValueError:
        return func.HttpResponse(
            json.dumps({"error": "Invalid JSON body"}),
            status_code=400,
            mimetype="application/json"
        )

    # Extract the question from the JSON body
    question = request_json.get("question")

    # Validate that the question field exists
    if not question:
        return func.HttpResponse(
            json.dumps({"error": "Missing 'question' field"}),
            status_code=400,
            mimetype="application/json"
        )

    # Call the RAG function
    result = ask_question(question)

    # Return the result as JSON
    return func.HttpResponse(
        json.dumps(result),
        status_code=200,
        mimetype="application/json"
    )
