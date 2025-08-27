"""Definitions of the tasks used by the CrewAI workflow."""

from crewai import Task

from agents import financial_analyst, verifier
from tools import FinancialDocumentTool, search_tool


analyze_financial_document = Task(
    description=(
        "Examine the provided financial document and address the user's query: {query}. "
        "Use the available tools to read the document and, when necessary, search "
        "reliable sources for additional context. Summarise key findings and "
        "present actionable insights."
    ),
    expected_output=(
        "A clear, structured analysis referencing relevant figures from the document and any "
        "supporting information found online."
    ),
    agent=financial_analyst,
    tools=[FinancialDocumentTool.read_data_tool, search_tool],
    async_execution=False,
)


investment_analysis = Task(
    description=(
        "Using the financial document, discuss possible investment opportunities and considerations "
        "related to the user's question: {query}."
    ),
    expected_output=(
        "A list of potential investment ideas with brief explanations and associated risk factors."
    ),
    agent=financial_analyst,
    tools=[FinancialDocumentTool.read_data_tool, search_tool],
    async_execution=False,
)


risk_assessment = Task(
    description=(
        "Review the document to identify significant risks or uncertainties relevant to {query}."
    ),
    expected_output=(
        "An overview of key risk factors and, where possible, suggestions for mitigating them."
    ),
    agent=financial_analyst,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False,
)


verification = Task(
    description=(
        "Verify that the uploaded file is a financial document and provide a short summary of its contents."
    ),
    expected_output="Confirmation of the document type and a brief summary of its key sections.",
    agent=verifier,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False,
)
