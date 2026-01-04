from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

# Ensure these modules exist in your directory
from rag_pipeline.rag_chain import RAGPipeline
from escalation.escalation_handler import check_escalation

app = FastAPI()

# Mounting the static directory correctly
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

# Initialize RAG
rag = RAGPipeline()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        question = data.get("question", "").strip()

        if not question:
            return JSONResponse({
                "answer": "Please enter a valid question.",
                "confidence": 0.0,
                "escalate": False
            })

        # Calling the RAG pipeline
        # Note: Use 'await rag.run(question)' if your run method is async
        response = rag.run(question)

        return JSONResponse({
            "answer": response.get("answer", "No answer found."),
            "confidence": response.get("confidence", 0.0),
            "escalate": check_escalation(response)
        })

    except Exception as e:
        print(f"Error: {e}") # Log error to terminal
        return JSONResponse({
            "answer": "⚠️ AI service temporarily unavailable.",
            "confidence": 0.0,
            "escalate": True
        }, status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)