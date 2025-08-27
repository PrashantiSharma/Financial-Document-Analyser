"""Definitions of the agents used by the application.

The original repository contained intentionally exaggerated and unsafe prompts
and also referenced an undefined LLM instance.  This module now provides a set
of responsible, professional agents powered by a small in-memory LLM stub so
that the code runs deterministically during tests without requiring external
API access.
"""

from dotenv import load_dotenv
from crewai.agents import Agent
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage
from langchain_core.outputs import ChatGeneration, ChatResult

from tools import FinancialDocumentTool

load_dotenv()


class DummyLLM(BaseChatModel):
    """A very small LLM stub used for testing.

    It simply returns a constant message.  This avoids network calls while still
    providing an object compatible with the interfaces expected by CrewAI.
    """

    def _generate(self, messages, stop=None, run_name=None, **kwargs) -> ChatResult:  # type: ignore[override]
        return ChatResult(generations=[ChatGeneration(message=AIMessage(content="LLM output not available in tests."))])

    @property
    def _llm_type(self) -> str:  # type: ignore[override]
        return "dummy"


llm = DummyLLM()


financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal=(
        "Analyse financial documents and answer the user's query: {query}. "
        "Provide factual, well reasoned insights and clearly communicate any "
        "uncertainties."
    ),
    verbose=True,
    memory=True,
    backstory=(
        "You have extensive experience interpreting financial statements and "
        "market trends.  Your advice is grounded in data and established "
        "financial principles."
    ),
    tools=[FinancialDocumentTool.read_data_tool],
    llm=llm,
    max_iter=3,
    max_rpm=3,
    allow_delegation=True,
)


verifier = Agent(
    role="Financial Document Verifier",
    goal=(
        "Confirm that supplied files are financial in nature and summarise key "
        "information relevant to the user's query."
    ),
    verbose=True,
    memory=True,
    backstory=(
        "Your background is in regulatory compliance.  You carefully review "
        "documents to ensure they are relevant and accurate."
    ),
    llm=llm,
    max_iter=2,
    max_rpm=3,
    allow_delegation=True,
)


investment_advisor = Agent(
    role="Investment Advisor",
    goal=(
        "Suggest suitable investment approaches based on the available "
        "financial information while outlining potential risks."
    ),
    verbose=True,
    backstory=(
        "You specialise in building diversified portfolios and adhere to "
        "industry best practices and regulations."
    ),
    llm=llm,
    max_iter=3,
    max_rpm=3,
    allow_delegation=False,
)


risk_assessor = Agent(
    role="Risk Assessment Specialist",
    goal=(
        "Identify and explain potential risks highlighted by the financial "
        "document. Provide balanced recommendations for mitigating those risks."
    ),
    verbose=True,
    backstory=(
        "You are experienced in risk management and help investors understand "
        "both the upside and downside of their decisions."
    ),
    llm=llm,
    max_iter=3,
    max_rpm=3,
    allow_delegation=False,
)
