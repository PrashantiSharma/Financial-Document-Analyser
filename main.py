"""FastAPI entry point for the Financial Document Analyzer."""

import os
import uuid

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from crewai import Crew, Process

from agents import financial_analyst
from task import analyze_financial_document
from tools import FinancialDocumentTool

app = FastAPI(title="Financial Document Analyzer")


def run_crew(query: str, file_path: str = "data/sample.pdf"):
    """Execute the CrewAI workflow for a given query and document."""

    # Ensure the document reader points to the correct file
    FinancialDocumentTool.default_path = file_path

    financial_crew = Crew(
        agents=[financial_analyst],
        tasks=[analyze_financial_document],
        process=Process.sequential,
    )
    return financial_crew.kickoff({"query": query})


@app.get("/")
async def root() -> dict:
    """Health check endpoint."""
    return {"message": "Financial Document Analyzer API is running"}


@app.post("/analyze")
async def analyze_financial_document_endpoint(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights"),
) -> dict:
    """Analyze a financial document and provide recommendations."""

    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"

    try:
        os.makedirs("data", exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        if not query:
            query = "Analyze this financial document for investment insights"

        response = run_crew(query=query.strip(), file_path=file_path)
        return {
            "status": "success",
            "query": query,
            "analysis": str(response),
            "file_processed": file.filename,
        }
    except Exception as e:  # pragma: no cover - defensive programming
        raise HTTPException(status_code=500, detail=f"Error processing financial document: {e}")
    finally:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except OSError:
                pass


if __name__ == "__main__":  # pragma: no cover - manual launch
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
