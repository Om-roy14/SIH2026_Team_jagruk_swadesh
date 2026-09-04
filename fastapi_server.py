from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from jagruk_brain_pipeline.main import app as pipeline_app

server = FastAPI()

server.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class QueryRequest(BaseModel):
    query: str

@server.post("/query")
def run_query(request: QueryRequest):
    initial_state = {
        "medium": "1",
        "raw_query": request.query
    }
    final_state = pipeline_app.invoke(initial_state)
    answer = final_state.get("final_answer", "No answer returned.")
    return {"answer": answer}

@server.get("/health")
def health():
    return {"status": "ok"}
