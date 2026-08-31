from fastapi import FastAPI
from pydantic import BaseModel
from Rag_agent import ask_rag, detect_product


app = FastAPI(
    title="BIS AI RAG API",
    description="BIS Regulatory & Certification RAG API",
    version="1.0.0"
)


# ============================================================
# REQUEST MODEL
# ============================================================

class QuestionRequest(BaseModel):
    question: str


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():
    return {
        "ready": True,
        "service": "BIS RAG",
        "status": "running"
    }


# ============================================================
# CHAT / ASK
# ============================================================

@app.post("/ask")
def ask(request: QuestionRequest):

    question = request.question.strip()

    if not question:
        return {
            "success": False,
            "message": "Question is required"
        }

    try:

        result = ask_rag(question)

        return result

    except Exception as e:

        print("RAG ERROR:", e)

        return {
            "success": False,
            "message": str(e)
        }


# ============================================================
# PRODUCT DETECTION
# ============================================================

@app.post("/detect-product")
def detect(request: QuestionRequest):

    question = request.question.strip()

    if not question:
        return {
            "success": False,
            "message": "Question is required"
        }

    try:

        product = detect_product(question)

        return {
            "success": True,
            "question": question,
            "detected_product": product
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }