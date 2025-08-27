"""Utility tools used by the financial analysis application."""

import os
from typing import Optional

from dotenv import load_dotenv
from pypdf import PdfReader
from crewai_tools.tools.serper_dev_tool import SerperDevTool

load_dotenv()

# Expose a simple web search tool used by some agents
search_tool = SerperDevTool()


class FinancialDocumentTool:
    """Utility class for reading financial documents.

    The class exposes ``read_data_tool`` which can be registered as a CrewAI
    tool.  The path of the document to analyse can be set via ``default_path``;
    ``main.run_crew`` updates this before the crew is executed.
    """

    # Default location of the PDF to read.  This value is overwritten at runtime
    # when the API receives an uploaded file.  Use the bundled Tesla report so
    # ``run_crew`` works out of the box.
    default_path: str = "data/TSLA-Q2-2025-Update.pdf"

    @staticmethod
    async def read_data_tool(path: Optional[str] = None) -> str:
        """Read and return the textual contents of a PDF file.

        Args:
            path: Optional path to the PDF file.  If not provided the value from
                :attr:`default_path` is used.

        Returns:
            The extracted text from the PDF.

        Raises:
            FileNotFoundError: If the file does not exist.
        """

        path = path or FinancialDocumentTool.default_path
        if not os.path.exists(path):
            raise FileNotFoundError(f"PDF file not found: {path}")

        reader = PdfReader(path)
        pages_text: list[str] = []
        for page in reader.pages:
            text = page.extract_text() or ""
            pages_text.append(text.strip())
        return "\n".join(pages_text).strip()


class InvestmentTool:
    """Placeholder for future investment analysis capabilities."""

    async def analyze_investment_tool(self, financial_document_data: str) -> str:
        processed_data = " ".join(financial_document_data.split())
        # TODO: Implement investment analysis logic
        return processed_data


class RiskTool:
    """Placeholder for future risk assessment capabilities."""

    async def create_risk_assessment_tool(self, financial_document_data: str) -> str:
        # TODO: Implement risk assessment logic
        return financial_document_data
