import traceback
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from services.preprocessing import clean_dataset
from services.llm_parser import parse_query
from services.query_executor import execute_query
from services.response_generator import generate_response

app = FastAPI()

# Load dataset 
df = clean_dataset("data/books_cleaned.csv")


class QueryRequest(BaseModel):
    question: str


# API Endpoint
@app.post("/ask")
def ask_question(request: QueryRequest):
    try:
        # Parse natural lang to structured query
        structured_query = parse_query(request.question)
        print("STRUCTURED QUERY:", structured_query)

        # query against DataFrame
        results = execute_query(df, structured_query)
        print("RESULTS COUNT:", len(results))

        # natural lang answer
        answer = generate_response(request.question, results)

        return {
            "response": answer,
            "metadata": results
        }

    except Exception as e:
        error_trace = traceback.format_exc()
        print("ERROR:", error_trace)  
        return JSONResponse(
            status_code=500,
            content={
                "error": str(e),
                "trace": error_trace
            }
        )